#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/wait.h>
#include <signal.h>
#include <fcntl.h>

#define MAX_PROCESSES 1000
/**
 * @brief Tokenize a C string 
 * 
 * @param str - The C string to tokenize 
 * @param delim - The C string containing delimiter character(s) 
 * @param argv - A char* array that will contain the tokenized strings
 * Make sure that you allocate enough space for the array.
 */

 void tokenize(char* str, const char* delim, char ** argv) {
  char* token;
  token = strtok(str, delim);
  for(size_t i = 0; token != NULL; ++i){
    argv[i] = token;
  token = strtok(NULL, delim);
  }
}

enum ProcessState {
  RUNNING,
  SUSPENDED,
  TERMINATED
};

struct Process {
  pid_t pid;
  enum ProcessState status;
  char *command;
};
struct Process processes[MAX_PROCESSES]; // Allocate memory for 100 processes
int process_count = 0; // Keep track of the number of processes
int background = 0; // Flag to indicate if the process should run in the background
int current_pid = 0; // Keep track of the current process ID
int re_input = -1;
int re_output = -1;
int pipe_ind = -1;

void remove_process() {
  for (int i = 0; i < process_count;) {
    if (processes[i].status == TERMINATED) {
      free(processes[i].command);
      for (int j = i; j < process_count - 1; j++) {
        processes[j] = processes[j + 1];
      }
      process_count--;
    } else {
      i++;
    }
  }
}
// --- SIGNAL HANDLERS --- //
void handle_sigint(int sig) {
  if (current_pid > 0) {
    kill(current_pid, SIGINT);
  } else {
    write(STDOUT_FILENO, "\nphoenixshell> ", 15);
  }
}

void handle_sigtstp(int sig) {
  if (current_pid > 0) {
    kill(current_pid, SIGTSTP);
  } else{
    write(STDOUT_FILENO, "\nphoenixshell> ", 15);
  }
}

void handle_sigchld(int sig) {
  //do not put removal here, free() is not async signal safe
  int saved_errno = errno; // Save errno to restore it later
  pid_t pid;
  int wait_status;

  // reap terminated child processes without blocking
  while ((pid = waitpid(-1, &wait_status, WNOHANG | WUNTRACED)) > 0) {
    // Find the process in the list and update its status
    for (int i = 0; i < process_count; i++) {
      if (processes[i].pid == pid) {
        if (WIFEXITED(wait_status) || WIFSIGNALED(wait_status)) {
          processes[i].status = TERMINATED;
        } else if (WIFSTOPPED(wait_status)) {
          processes[i].status = SUSPENDED;
        }
        break;
      }
    }
  }

  errno = saved_errno; // Restore errno
}


// --- BUILT-IN COMMANDS --- //
void run_pwd() {
  char cwd[1024];
  if (getcwd(cwd, sizeof(cwd)) != NULL) {
    printf("%s\n", cwd);
  } else {
    perror("phoenixshell");
  }
}

void run_cd(char **args) {
  if (args[1] == NULL) {
    fprintf(stderr, "phoenixshell: Expected argument to \"cd\"\n");
  } else {
    if (chdir(args[1]) != 0) {
      perror("phoenixshell");
    }
  }
}

void run_jobs() {
  //printf("ID PID STATUS CMD\n");
  for (int i = 0; i < process_count; i++) {
    const char *status_name;
    switch (processes[i].status) {
      case RUNNING:
        status_name = "R";
        break;
      case SUSPENDED:
        status_name = "T";
        break;
      case TERMINATED:
        status_name = "TERMINATED";
        break;
      default:
        status_name = "UNKNOWN";
        break;
    }
    printf("[%d] %d %s %s\n",
      i + 1,
      processes[i].pid,
      status_name,
      processes[i].command);
  }
}

void run_bg(char **args) {
  if (args[1] == NULL) {
    fprintf(stderr, "phoenixshell: bg: Expected argument\n");
    return;
  }

  int index = atoi(args[1]);
  index--;

  if (index < 0 || index >= process_count) {
    fprintf(stderr, "phoenixshell: bg: job index not found\n");
    return;
  }

  if (processes[index].status == SUSPENDED) {
    kill(processes[index].pid, SIGCONT);
    processes[index].status = RUNNING;
    struct Process resumed_process = processes[index];
    for (int i = index; i < process_count - 1; i++) {
      processes[i] = processes[i + 1];
    }
    processes[process_count - 1] = resumed_process;
    printf("Process %d is sent to background\n", resumed_process.pid);
  } else {
    fprintf(stderr, "phoenixshell: bg: job already running\n");
  }
}

void run_fg(char **args) {
  if (args[1] == NULL) {
    fprintf(stderr, "phoenixshell: fg: Expected argument\n");
    return;
  }

  int index = atoi(args[1]);
  index--;

  if (index < 0 || index >= process_count) {
    fprintf(stderr, "phoenixshell: fg: job index not found\n");
    return;
  }

  if (processes[index].status == SUSPENDED) {
    kill(processes[index].pid, SIGCONT);
    processes[index].status = RUNNING;
  }

  current_pid = processes[index].pid;
  int status;
  waitpid(current_pid, &status, WUNTRACED);
  current_pid = 0;

  if (WIFEXITED(status) || WIFSIGNALED(status)) {
    processes[index].status = TERMINATED;
    remove_process();
  } else if (WIFSTOPPED(status)) {
    processes[index].status = SUSPENDED;
  }
}

int main(int argc, char **argv) {

  // signal handler for SIGCHLD
  sigset_t sigchld_mask;
  sigemptyset(&sigchld_mask);
  sigaddset(&sigchld_mask, SIGCHLD);

  struct sigaction sa;
  sa.sa_handler = handle_sigchld;
  sigemptyset(&sa.sa_mask);
  sa.sa_flags = SA_RESTART;
  if (sigaction(SIGCHLD, &sa, NULL) == -1) {
    perror("sigaction");
    exit(1);
  }

  struct sigaction sa_tstp;
  sa_tstp.sa_handler = handle_sigtstp;
  sigemptyset(&sa_tstp.sa_mask);
  sa_tstp.sa_flags = SA_RESTART;
  if (sigaction(SIGTSTP, &sa_tstp, NULL) == -1) {
    perror("sigaction");
    exit(1);
  }
  
  struct sigaction sa_int;
  sa_int.sa_handler = handle_sigint;
  sigemptyset(&sa_int.sa_mask);
  sa_int.sa_flags = SA_RESTART;
  if (sigaction(SIGINT, &sa_int, NULL) == -1) {
    perror("sigaction");
    exit(1);
  }

  while (1) {
    // receive
    printf("phoenixshell> ");
    char input[1024];
    char original_cmd[1024];
    // convert
    if(fgets(input, sizeof(input), stdin) == NULL) {
      if (errno == EINTR) {
        clearerr(stdin); 
        continue;
      } 
    }
    input[strcspn(input, "\n")] = '\0';
    strncpy(original_cmd, input, sizeof(original_cmd)-1);
    char *args[100] = {NULL};
    tokenize(input, " \n", args);

    for (int i = 0; args[i] != NULL; i++) {
      int len = strlen(args[i]);

      if (len >= 2 && args[i][0] == '"' && args[i][len - 1] == '"') {
        args[i][len - 1] = '\0';
        args[i]++;
      }
    }
    // reset redirection and pipe indicators
    re_input = -1;
    re_output = -1;
    pipe_ind = -1;
    
    //determine bg process and redirect
    int cmdlen = 0;
    while (args[cmdlen] != NULL) {
      if (strcmp(args[cmdlen], "<") == 0) {
        re_input = cmdlen;
      }

      if (strcmp(args[cmdlen], ">") == 0) {
        re_output = cmdlen;
      }

      if (strcmp(args[cmdlen], "|") == 0) {
        pipe_ind = cmdlen;
      }
      cmdlen++;
    }
    
    if (cmdlen > 0 && strcmp(args[cmdlen - 1], "&") == 0) {
      background = 1;
      args[cmdlen - 1] = NULL; // Remove the '&' from the arguments
    } else {
      background = 0;
    }

    if (args[0] == NULL) {
      continue;
    }
    else if (strcmp(args[0], "pwd") == 0) {
      run_pwd();
    }
    else if (strcmp(args[0], "cd") == 0) {
      run_cd(args);
    }
    else if (strcmp(args[0], "jobs") == 0) {
      remove_process();
      run_jobs();
    }
    else if (strcmp(args[0], "bg") == 0) {
      remove_process();
      run_bg(args);
    }
    else if (strcmp(args[0], "fg") == 0) {
      remove_process();
      run_fg(args);
    }
    else if (strcmp(args[0], "exit") == 0) {
      for (int i = 0; i < process_count; i++) {
        kill(processes[i].pid, SIGTERM);
        free(processes[i].command);
      }
      break;
    }
    else {
      sigprocmask(SIG_BLOCK, &sigchld_mask, NULL); // Block SIGCHLD signals

      if (pipe_ind != -1) {
          int pipefd[2];
          if (pipe(pipefd) == -1) {
            perror("pipe");
            exit(EXIT_FAILURE);
          }

          pid_t pipe_pid = fork();
          if (pipe_pid == 0) { 
            close(pipefd[1]);
            dup2(pipefd[0], STDIN_FILENO);
            close(pipefd[0]); 
            execve(args[pipe_ind + 1], &args[pipe_ind + 1], NULL);
            _exit(1); 
          }
          pid_t pipe_pid2 = fork();
          if (pipe_pid2 == 0) { 
            close(pipefd[0]);
            dup2(pipefd[1], STDOUT_FILENO);
            close(pipefd[1]);
            args[pipe_ind] = NULL;
            execve(args[0], args, NULL);
            _exit(1);
          } 
          close(pipefd[0]);
          close(pipefd[1]);
          waitpid(pipe_pid, NULL, 0);
          waitpid(pipe_pid2, NULL, 0);
        } else {
          pid_t pid = fork();
          if (pid == 0) { // Child process
            if (re_input != -1) {
              int input_fd = open(args[re_input + 1], O_RDONLY);
              dup2(input_fd, STDIN_FILENO);
              close(input_fd);
              args[re_input] = NULL;
            }
            if (re_output != -1) {
              int output_fd = open(args[re_output + 1], O_WRONLY | O_CREAT | O_TRUNC, 0644);
              dup2(output_fd, STDOUT_FILENO);
              close(output_fd);
              args[re_output] = NULL;
            }   
            execve(args[0], args, NULL);
            printf("phoenixshell: command not found: %s\n", args[0]);
            _exit(1); // If execve fails, exit the child process
          } else if (pid > 0) { // Parent process
          setpgid(pid, pid);
          struct Process new_process = {pid, RUNNING, strdup(original_cmd)};
          processes[process_count] = new_process;
          process_count++;

          int status;
          // Wait for the child process to terminate
          if (!background) {
            current_pid = pid;
            waitpid(pid, &status, WUNTRACED);
            current_pid = 0;
            if (WIFEXITED(status) || WIFSIGNALED(status)) {
              processes[process_count - 1].status = TERMINATED;
              remove_process();
            } else if (WIFSTOPPED(status)) {
              processes[process_count - 1].status = SUSPENDED;
            }
          } else {
            printf("PID %d is sent to background\n", pid);
          }
        } else { // Fork failed
          perror("phoenixshell");
        }
        sigprocmask(SIG_UNBLOCK, &sigchld_mask, NULL);
      }
    }
  }
  return 0;
}