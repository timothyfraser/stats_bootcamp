# K0_example.R

# Load packages
library(dplyr)
library(readr)
library(ggplot2)

# Load data - 1000 sampled diamond prices and their sizes
data = read_csv("K/diamonds_sample.csv")

# view it!
data

# Plot the scatterplot with a line of best fit!
ggplot() +
  geom_point(data = data, mapping = aes(x = carat, y = price)) +
  geom_smooth(data = data, mapping = aes(x = carat, y = price),
              method = "lm", se = FALSE, color = "steelblue")


# Model it!
m = lm(formula = price ~ carat, data = data)

# View it!
m

# View model table
summary(m)


# Cleanup!
rm(list = ls())
