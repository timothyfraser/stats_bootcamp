# P1_code.R
# Correlation with Pearson's r 
# Tim Fraser

# This tutorial introduces the correlation coefficient Pearson's r,
# which evaluates the relationship between two numeric variables.

# Import necessary libraries
# !pip install pandas
# !pip install pingouin

# Load packages
import pandas as pd
import pingouin as pg

# Load in the penguins data!
penguins = pd.read_csv("P/palmerpenguins.csv")

# Researchers tracked 344 penguins in Antarctica, from 2007 to 2009.
# We want to know, are traits of these penguins changing over time?

# We'll use the pg.corr() function in Python to calculate the Pearson's r correlation coefficient
# This statistic ranges from -1 to 1, where:
#   -1 = perfect negative relationship, 
#   0 = no relationship
#   1 = perfect positive relationship
# This test also calculates a t-statistic for that correlation,
# to evaluate how statistically significant is that correlation.

# Let's use cor.test() to assess whether penguins' body mass is 
# positively/negatively related to the year of observation.
stat = pg.corr(x = penguins.year, y = penguins.body_mass_g, method = "pearson") 

# View table
stat

# Let's extract some stats! 
stat['r'] # view the correlation coefficient itself
# that's a very weak, minimal, positive correlation

stat['p-val'] # view p-value for t-statistic (t-statistic itself not included in result)
# very large - ~57% of random correlations / t-statistics are greater than this one.

stat['CI95%'] # view 95% confidence interval for estimate
# If our data was just slightly different due to chance,
# 95% of the time, the Pearson's r correlation coefficient would be within this range.


# Let's assess some other traits too.


# Is year related to a penguin's body mass?
pg.corr(x = penguins.year, y = penguins.body_mass_g, method = "pearson")
# Is year related to a penguin's flipper length?
pg.corr(x = penguins.year, y = penguins.flipper_length_mm, method = "pearson")
# Is year related to a penguin's bill depth?
pg.corr(x = penguins.year, y = penguins.bill_depth_mm, method = "pearson")
# Is year related to a penguin's bill length
pg.corr(x = penguins.year, y = penguins.bill_length_mm, method = "pearson")

# Looks like the strongest correlation is between year and flipper length
# r = +0.170 
# t = 3.17
# p < 0.01

# No other associations were statistically significant.


# Cleanup!
globals().clear()
