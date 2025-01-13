# K2_code.py
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



# 2. Model the effect of each year on income. 
# Which year is not represented? The intercept represents that baseline category.
cities.year.unique() # see unique values
m = sm.formula.ols(formula = 'income_per_capita ~ year_2012 + year_2013 + year_2014 + year_2015 + year_2016 + year_2017', data = cities).fit()
m.summary()





# 3. Estimate the effect of being hit by the tsunami on income per capita, 
# controlling for damage rates.
m = sm.formula.ols(formula = 'income_per_capita ~ damage_rate + by_tsunami', data = cities).fit()

m.summary()

# Report the effect of being hit by the tsunami.
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# This effect has a 95% confidence interval from [A] to [B].
# This effect is statistically [significant? insignificant?] with a p-value of [XXX].





# 4. Model the effect of time on income per capita, 
# controlling for relevant traits.
m1 = sm.formula.ols(formula = 'income_per_capita ~ pop_density + unemployment + damage_rate + by_tsunami + year', data = cities).fit()

m2 = sm.formula.ols(formula = 'income_per_capita ~ pop_density + unemployment + damage_rate + by_tsunami + year_2012 + year_2013 + year_2014 + year_2015 + year_2016 + year_2017', data = cities).fit()


# View the resulting statistical table. 
# How does the information change when we control for year vs. each year? 
m1.summary()
m2.summary()





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
m = sm.formula.ols(
    formula = 'income_per_capita ~ pop_density + unemployment + damage_rate + by_tsunami + year_2012 + year_2013 + year_2014 + year_2015 + year_2016 + year_2017', 
    data = cities2).fit()

# Report the population density vs. unemployment, damage_rate
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# Which effect size is largest?
# Which effect sizes can you NOT compare?


# Cleanup!
globals().clear()
