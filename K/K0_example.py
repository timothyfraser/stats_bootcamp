# K0_example.py
# Example for class slides

# Install
# !pip install pandas
# !pip install plotnine
# !pip install statsmodel

# Load packages
import pandas as pd
from plotnine import *
import statsmodels.api as sm

# Import dataset, which is a bunch of diamonds!
data = pd.read_csv("K/diamonds_sample.csv")


# *Because we took a random sample, 
# your results will differ slightly each time the code is run.

# View the price and size (carats) of each diamond
data


# Let's plot the line of best fit in ggplot

( ggplot() + 
  geom_point(data = data, mapping = aes(x = 'carat', y = 'price')) +
  geom_smooth(data = data, mapping = aes(x = 'carat', y = 'price'),
    se = False, method = 'lm', color = 'steelblue')
) 


# Make a linear model (aka ordinary least squares OLS)
m = sm.formula.ols(formula = 'price ~ carat', data = data).fit()

# View results
m.summary()



# Cleanup!
globals().clear()
