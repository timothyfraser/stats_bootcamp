# J1_code.R
# Correlation with Pearson's r 
# Tim Fraser

# This tutorial introduces the correlation coefficient Pearson's r,
# which evaluates the relationship between two numeric variables.

# Load packages
library(dplyr)
library(readr)
library(broom)

# Load in the penguins data!
penguins = read_csv("J/palmerpenguins.csv")

# Researchers tracked 344 penguins in Antarctica, from 2007 to 2009.
# We want to know, are traits of these penguins changing over time?

# We'll use the cor.test() function in R to calculate the Pearson's r correlation coefficient
# This statistic ranges from -1 to 1, where:
#   -1 = perfect negative relationship, 
#   0 = no relationship
#   1 = perfect positive relationship
# This test also calculates a t-statistic for that correlation,
# to evaluate how statistically significant is that correlation.

# Let's use cor.test() to assess whether penguins' body mass is 
# positively/negatively related to the year of observation.
m = cor.test(x = penguins$year, y = penguins$body_mass_g, method = "pearson") 

# Let's extract a data.frame of results with the broom package's tidy() function
stat = broom::tidy(m)
# View table
stat

# Let's extract some stats! 
stat$estimate # view the correlation coefficient itself
# that's a very weak, minimal, positive correlation

stat$statistic # view t-statistic
# small, positive, less than ~2, the simple eye-ball benchmark for significance

stat$p.value # view p-value for t-statistic
# very large - ~57% of random t-statistics are greater than this one.

c(stat$conf.low, stat$conf.high) # view 95% confidence interval for estimate
# If our data was just slightly different due to chance,
# 95% of the time, the Pearson's r correlation coefficient would be within this range.


# Let's assess some other traits too.

# Is year related to a penguin's body mass?
cor.test(x = penguins$year, y = penguins$body_mass_g, method = "pearson") %>% broom::tidy()
# Is year related to a penguin's flipper length?
cor.test(x = penguins$year, y = penguins$flipper_length_mm, method = "pearson") %>% broom::tidy()
# Is year related to a penguin's bill depth?
cor.test(x = penguins$year, y = penguins$bill_depth_mm, method = "pearson") %>% broom::tidy()
# Is year related to a penguin's bill length
cor.test(x = penguins$year, y = penguins$bill_length_mm, method = "pearson") %>% broom::tidy()

# Looks like the strongest correlation is between year and flipper length
# r = +0.170 
# t = 3.17
# p < 0.01

# No other associations were statistically significant.


# Cleanup!
rm(list = ls())
