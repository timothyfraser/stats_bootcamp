# K2_code.py
# Multivariate Regression in Python
# Exercise


# Load packages
import pandas as pd
import statsmodels.api as sm


# Our data about disaster outcomes in Japanese municipalities over time
cities = pd.read_csv("K/jp_matching_experiment.csv")

# Make by_tsunami a binary variable where 1 means hit by tsunami
cities['by_tsunami'] = cities.by_tsunami == "Hit"
# Make categorical variable into a series of binary variables per year
cities['year_2011'] = cities.year == 2011
cities['year_2012'] = cities.year == 2012
cities['year_2013'] = cities.year == 2013
cities['year_2014'] = cities.year == 2014
cities['year_2015'] = cities.year == 2015
cities['year_2016'] = cities.year == 2016
cities['year_2017'] = cities.year == 2017


# View columns
cities.columns

# View data
cities




# 1. Compare these two data.frames. 
# What does it mean to estimate an intercept-only model?

# Intercept-only model
m = sm.formula.ols(formula = 'income_per_capita ~ 1', data = cities).fit()
m.summary()
# Descriptive Stats
cities.income_per_capita.mean()




# Answers:
# An intercept-only model predicts the outcome 
# by literally taking the mean of the outcome.







# 2. Model the effect of each year on income. 
# Which year is not represented? The intercept represents that baseline category.
cities.year.unique() # see unique values
m = sm.formula.ols(formula = 'income_per_capita ~ year_2012 + year_2013 + year_2014 + year_2015 + year_2016 + year_2017', data = cities).fit()
m.summary()






# Answers:
# 2011 is not represented; 2011 is the baseline category for comparison.
# 1.056 + -0.0336 --> 1.0224 in 2012
# ...
# 1.056 + 0.1021  --> 1.1581 in 2017







# 3. Estimate the effect of being hit by the tsunami on income per capita, 
# controlling for damage rates.
m = sm.formula.ols(formula = 'income_per_capita ~ damage_rate + by_tsunami', data = cities).fit()

m.summary()

# Report the effect of being hit by the tsunami.
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# This effect has a 95% confidence interval from [A] to [B].
# This effect is statistically [significant? insignificant?] with a p-value of [XXX].








# Answers:

# Report the effect of being hit by the tsunami.
# When hit by the tsunami (1 vs. 0), the income per capita in millions of yen per capita 
# increases by +0.032 millions of yen per capita.
# This effect has a 95% confidence interval from -0.001 to 0.066.
# This effect is statistically **insignificant?** at a 95% confidence level, with a p-value of 0.058.
# This effect is statistically significant at a 90% confidence level, because 0.058 < p = 0.10.







# 4. Model the effect of time on income per capita, 
# controlling for relevant traits.
m1 = sm.formula.ols(formula = 'income_per_capita ~ pop_density + unemployment + damage_rate + by_tsunami + year', data = cities).fit()

m2 = sm.formula.ols(formula = 'income_per_capita ~ pop_density + unemployment + damage_rate + by_tsunami + year_2012 + year_2013 + year_2014 + year_2015 + year_2016 + year_2017', data = cities).fit()


# View the resulting statistical table. 
# How does the information change when we control for year vs. each year? 
m1.summary()
m2.summary()


# See video for discussion.



# 5. Normalize these demographic covariates
# (mean = 0, in units of standard deviation from the mean)
# Use the scale function below. Now model them. 
def scale(x):
  x = pd.Series(x)
  output = (x - x.mean() ) / x.std()
  return output

cities2 = cities
cities2['pop_density'] = scale(cities.pop_density)
cities2['unemployment'] = scale(cities.unemployment)
cities2['damage_rate'] = scale(cities.damage_rate)

# cities2.damage_rate.describe()

m = sm.formula.ols(
    formula = 'income_per_capita ~ pop_density + unemployment + damage_rate + by_tsunami + year_2012 + year_2013 + year_2014 + year_2015 + year_2016 + year_2017', 
    data = cities2).fit()

m.summary()

# Report the population density vs. unemployment, damage_rate
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# Which effect size is largest?
# Which effect sizes can you NOT compare?





# Answers:

# As the population density increases by 1 standard deviation,
# the income per capita is expected to increase by 0.18 millions of yen per capita.

# As the unemployment rate increases by 1 standard deviation,
# the income per capita is expected to decrease by 0.05 millions of yen per capita.

# As the damage rate increases by 1 standard deviation,
# the income per capita is expected to decrease by 0.01 millions of yen per capita.

# You can compare pop_density, unemployment, and damage_rate,
# because they are all in units of standard deviations.

# You can't compare effects of numeric predictors against effects of categorical predictors,
# because they're fundamentally different - eg. standard deviations versus 0/1



# Cleanup!
globals().clear()
