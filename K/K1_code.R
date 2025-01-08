# K1_code.R
# Exercise: Modeling Carbon Footprints in Japanese Cities
# Prof. Tim Fraser

# In this dataset, each row is a year, 
# representing the average carbon footprint 
# among Japanese municipalities that year.
# carbon footprint is measured as tons of emissions per 1000 residents,
# for just cities where anyone lives.

# install packages:
# install.packages(c("dplyr", "readr", "ggplot2", "broom"))

# Load packages
library(dplyr)
library(readr)
library(ggplot2)
library(broom)


# Import data
avg = read_csv("K/avg_annual_footprint.csv")


# Plot the raw data, using geom_point() and geom_line(). 
# What do we observe?
gg = ggplot() +
  geom_point(data = avg, mapping = aes(x = year, y = footprint)) +
  geom_line(data = avg, mapping = aes(x = year, y = footprint))


# Plot a line of best fit with ggplot() over it, using geom_smooth()
# What is the overall trend?
gg +
  geom_smooth(data = avg, mapping = aes(x = year, y = footprint), 
              method = "lm", se = FALSE)




# Task 1: Modeling #################################

# Calculate the model equation for that line of best fit, 
# using your dataframe avg and the lm() function.
# What rate of emissions was an average Japanese city projected
# to produce in the year 0 CE? 
# How much does the average carbon footprint increase 
# with every passing year, according to your model’s beta coeficient?


# The average Japanese city was projected to produce -307.27 kilotons
# of carbon emissions per 1000 residents in the year CE. 
# With every passing year, the average carbon footprint increases
# by 0.16 kilotons per 1000 residents.


# Task 2: Model Fit ################################

# Examine the model table, using summary() or broom::tidy().
# How likely is it that these two statistics were just that extreme by chance?

# The alpha coefficient, -307.27, was so extreme that there is 
# just a 0.036 probability (3.6% chance) that this statistic 
# occurred due to chance. 
# The effect of each year (beta = 0.16) 
# was so extreme that there is just a 0.031 probability (3.1% chance)
# that this statistic occurred due to chance. 
# Both effects are therefore statistical significant
# at the p < 0.05 level.


# Task 3: Model Fit ###################################

# Evaluate this model, using summary() or broom::glance().
# What percentage of variation in average carbon footprints
# does it explain? Does it fit better than an intercept model? 
# Is this model’s F statistic statistically significant? 
# How do you know?


# This model explained 39% of the variation 
# in average carbon footprints (R2 = 0.39). 
# It fits much better than an intercept model, 
# according to its F-statistic value of ``6.26. 
# In fact, there’s just a 0.031 probability (3.1% chance)
# that this statistic occurred due to chance, 
# so we can be at least 96.9% confident that this statistic did not 
# occur due to chance. 
# This model has a statistically significant fit.
  





