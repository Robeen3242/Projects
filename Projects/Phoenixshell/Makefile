CC = gcc
CFLAGS = -Wall

phoenixshell: compile
	$(CC) $(CFLAGS) phoenixshell.o -o phoenixshell

compile:
	$(CC) $(CFLAGS) -c phoenixshell.c -o phoenixshell.o

clean:
	rm -f phoenixshell.o phoenixshell
