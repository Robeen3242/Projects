# League of Legends Item Viability Analyzer
# =================================================

# Load required libraries
library(tidyverse)
library(ggplot2)
library(dplyr)
library(readr)

# =================================================
# 1. DATA LOADING AND PREPARATION
# =================================================

# Function to load and validate the CSV data
load_lol_data <- function(filepath) {
  cat("Loading data from:", filepath, "\n")
  
  # Read CSV file
  data <- tryCatch({
    read_csv(filepath, show_col_types = FALSE)
  }, error = function(e) {
    stop("Error reading CSV file: ", e$message)
  })
  
  cat("Data loaded successfully. Dimensions:", dim(data), "\n")
  cat("Columns:", paste(names(data), collapse = ", "), "\n\n")
  
  return(data)
}

# Function to clean and validate data
clean_data <- function(data) {
  cat("Cleaning data...\n")
  
  # Remove rows with missing values in critical columns
  data_clean <- data %>%
    drop_na(champion, item, win_rate, games_played)
  
  # Ensure win_rate is between 0 and 100 (or 0 and 1)
  if (max(data_clean$win_rate, na.rm = TRUE) > 1) {
    # Assume win_rate is in percentage form
    data_clean <- data_clean %>%
      mutate(win_rate_pct = win_rate,
             win_rate_decimal = win_rate / 100)
  } else {
    # Win_rate is already in decimal form
    data_clean <- data_clean %>%
      mutate(win_rate_decimal = win_rate,
             win_rate_pct = win_rate * 100)
  }
  
  cat("Cleaned data. Rows removed:", nrow(data) - nrow(data_clean), "\n")
  cat("Final dimensions:", dim(data_clean), "\n\n")
  
  return(data_clean)
}

# =================================================
# 2. ANALYSIS FUNCTIONS
# =================================================

# Get top items by win rate for a specific champion
get_top_items_for_champion <- function(data, champ_name, top_n = 10) {
  data %>%
    filter(champion == champ_name) %>%
    arrange(desc(win_rate_pct)) %>%
    head(top_n) %>%
    select(champion, item, win_rate_pct, games_played)
}

# Get champions with highest win rate for a specific item
get_best_champions_for_item <- function(data, item_name, top_n = 10) {
  data %>%
    filter(item == item_name) %>%
    arrange(desc(win_rate_pct)) %>%
    head(top_n) %>%
    select(champion, item, win_rate_pct, games_played)
}

# Calculate overall statistics
calculate_overall_stats <- function(data) {
  overall <- data %>%
    summarise(
      total_combinations = n(),
      avg_win_rate = mean(win_rate_pct, na.rm = TRUE),
      median_win_rate = median(win_rate_pct, na.rm = TRUE),
      sd_win_rate = sd(win_rate_pct, na.rm = TRUE),
      min_win_rate = min(win_rate_pct, na.rm = TRUE),
      max_win_rate = max(win_rate_pct, na.rm = TRUE)
    )
  
  cat("\n=== OVERALL STATISTICS ===\n")
  print(overall)
  cat("\n")
  
  return(overall)
}

# Find most popular items
get_most_popular_items <- function(data, top_n = 15) {
  data %>%
    group_by(item) %>%
    summarise(
      total_games = sum(games_played, na.rm = TRUE),
      avg_win_rate = mean(win_rate_pct, na.rm = TRUE),
      num_champions = n_distinct(champion)
    ) %>%
    arrange(desc(total_games)) %>%
    head(top_n)
}

# Find champions with highest overall win rates
get_top_champions <- function(data, top_n = 15) {
  data %>%
    group_by(champion) %>%
    summarise(
      avg_win_rate = mean(win_rate_pct, na.rm = TRUE),
      total_games = sum(games_played, na.rm = TRUE),
      num_items = n_distinct(item)
    ) %>%
    arrange(desc(avg_win_rate)) %>%
    head(top_n)
}

# =================================================
# 3. VISUALIZATION FUNCTIONS
# =================================================

# Plot top items for a champion
plot_champion_items <- function(data, champ_name, top_n = 15) {
  plot_data <- get_top_items_for_champion(data, champ_name, top_n)
  
  ggplot(plot_data, aes(x = reorder(item, win_rate_pct), y = win_rate_pct)) +
    geom_col(fill = "steelblue", alpha = 0.8) +
    geom_text(aes(label = sprintf("%.1f%%", win_rate_pct)), 
              hjust = -0.1, size = 3) +
    coord_flip() +
    labs(
      title = paste("Top", top_n, "Items for", champ_name),
      x = "Item",
      y = "Win Rate (%)"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
      axis.text = element_text(size = 10)
    ) +
    ylim(0, max(plot_data$win_rate_pct) * 1.1)
}

# Plot win rate distribution
plot_winrate_distribution <- function(data) {
  ggplot(data, aes(x = win_rate_pct)) +
    geom_histogram(bins = 50, fill = "darkgreen", alpha = 0.7, color = "black") +
    geom_vline(aes(xintercept = mean(win_rate_pct)), 
               color = "red", linetype = "dashed", size = 1) +
    labs(
      title = "Distribution of Win Rates (All Champion-Item Combinations)",
      x = "Win Rate (%)",
      y = "Frequency"
    ) +
    theme_minimal() +
    theme(plot.title = element_text(hjust = 0.5, face = "bold"))
}

# Plot top champions by average win rate
plot_top_champions <- function(data, top_n = 15) {
  plot_data <- get_top_champions(data, top_n)
  
  ggplot(plot_data, aes(x = reorder(champion, avg_win_rate), y = avg_win_rate)) +
    geom_col(fill = "coral", alpha = 0.8) +
    geom_text(aes(label = sprintf("%.1f%%", avg_win_rate)), 
              hjust = -0.1, size = 3) +
    coord_flip() +
    labs(
      title = paste("Top", top_n, "Champions by Average Win Rate"),
      x = "Champion",
      y = "Average Win Rate (%)"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
      axis.text = element_text(size = 10)
    ) +
    ylim(0, max(plot_data$avg_win_rate) * 1.1)
}

# =================================================
# 4. MAIN EXECUTION
# =================================================

# Example usage:
# Replace 'your_data.csv' with your actual CSV file path
main <- function(csv_file = "lol_champion_items.csv") {
  
  cat("=== LEAGUE OF LEGENDS WIN RATE ANALYSIS ===\n\n")
  
  # Load data
  data <- load_lol_data(csv_file)
  
  # Clean data
  data_clean <- clean_data(data)
  
  # Calculate overall statistics
  overall_stats <- calculate_overall_stats(data_clean)
  
  # Get most popular items
  cat("\n=== TOP 15 MOST POPULAR ITEMS ===\n")
  popular_items <- get_most_popular_items(data_clean, 15)
  print(popular_items)
  
  # Get top champions
  cat("\n=== TOP 15 CHAMPIONS BY WIN RATE ===\n")
  top_champs <- get_top_champions(data_clean, 15)
  print(top_champs)
  
  # Create visualizations
  cat("\nGenerating visualizations...\n")
  
  # Plot 1: Win rate distribution
  p1 <- plot_winrate_distribution(data_clean)
  print(p1)
  
  # Plot 2: Top champions
  p2 <- plot_top_champions(data_clean, 15)
  print(p2)
  
  # Plot 3: Example - top items for a specific champion
  # Get the champion with most data
  sample_champion <- data_clean %>%
    count(champion, sort = TRUE) %>%
    slice(1) %>%
    pull(champion)
  
  cat("\nShowing top items for:", sample_champion, "\n")
  p3 <- plot_champion_items(data_clean, sample_champion, 15)
  print(p3)
  
  cat("\n=== ANALYSIS COMPLETE ===\n")
  
  return(data_clean)
}

# =================================================
# 5. EXAMPLE DATA GENERATOR (FOR TESTING)
# =================================================

# Function to generate sample data without csv
generate_sample_data <- function(filename = "lol_champion_items.csv") {
  set.seed(123)
  
  champions <- c("Ahri", "Yasuo", "Zed", "Lux", "Jinx", "Thresh", "Lee Sin", 
                 "Vayne", "Darius", "Garen", "Katarina", "Ezreal")
  items <- c("Infinity Edge", "Rabadon's Deathcap", "Trinity Force", 
             "Guardian Angel", "Blade of the Ruined King", "Morellonomicon",
             "Zhonya's Hourglass", "Black Cleaver", "Warmog's Armor",
             "Thornmail", "Kraken Slayer", "Galeforce", "Immortal Shieldbow")
  
  # Generate all combinations
  data <- expand.grid(
    champion = champions,
    item = items,
    stringsAsFactors = FALSE
  )
  
  # Add random win rates and games played
  data$win_rate <- runif(nrow(data), 45, 55)
  data$games_played <- sample(100:10000, nrow(data), replace = TRUE)
  
  # Add some correlation (better items tend to have higher win rates)
  item_quality <- runif(length(items), 0.9, 1.1)
  names(item_quality) <- items
  data$win_rate <- data$win_rate * item_quality[data$item]
  
  # Ensure win rates are reasonable
  data$win_rate <- pmin(pmax(data$win_rate, 42), 58)
  
  write_csv(data, filename)
  cat("Sample data generated:", filename, "\n")
  cat("You can now run: result <- main('", filename, "')\n", sep = "")
}

# =================================================
# RUN THE ANALYSIS
# =================================================

# Uncomment this line to generate sample data (no CSV available):
# generate_sample_data("lol_champion_items.csv")

# Run the main analysis (replace with filename):
# result <- main("lol_champion_items.csv")