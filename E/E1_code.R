# E1_code.R
# Measuring Environmental Racism

# For Learning Checks, you can try out your code in here!

# Please load our main packages
library(dplyr) # data wrangling
library(readr) # inferential statistics
library(broom) # colors!

# Load data
counties <- read_csv("E/environmental_health.csv")

# View first 3 rows of dataset
counties %>% head(3)

