# L/L1_code.py
# Prediction

# We're going to try to predict food deserts!

# Scientists, engineers, policy analysts, and coders often
# have vitally important findings to convey to key decision-makers, 
# but it can be very difficult to convey that information quickly, 
# concisely, and in a visually appealing way. 

# Instead of telling policymakers about our beta-coefficients, 
# what if we could show them what our model predicts instead? 
# Exactly how many more lives can we affect, dollars can we earn, 
# emissions can we cut, if we adopt policy A instead of B, 
# or increase our level of spending by $1000? 

# We can answer these kinds of questions using statistical simulation.

# Background #############################

# This tutorial introduces statistical simulation using the example of
# the Food Environment Index from the 
# University of Wisconsin’s County Health Rankings, 
# which measures access to healthy foods in each county. 

# Food Environment Index:
# An Index of factors that contribute to a healthy food environment, 
# from 0 (worst) to 10 (best).

# Read more about the food environment index here!
# https://www.countyhealthrankings.org/health-data/health-factors/health-behaviors/diet-and-exercise/food-environment-index?year=2024

# Using just a few covariates, we estimate the relationship 
# between key demographic traits and access to healthy foods. 
# This workshop highlights how racial and ethnic minorities groups 
# face systemic barriers to health, like “food deserts”, 
# which describe when our cities’ urban planning has
# sited grocery stores and food infrastructure 
# far away from certain communities -
# often communities of color and low-income communities.
# But can we show these trends with data?


# 0. Getting Started ###############################

# Install packages if needed
# !pip install pandas
# !pip install scipy
# !pip install plotnine
# !pip install statsmodels


# Load Packages
import pandas as pd
from plotnine import *
import statsmodels.api as sm
# Import these functions from scipy.stats package
from scipy.stats import norm

# Load data - county outcomes and traits in 2019
counties = pd.read_csv("L/food_deserts.csv")

# View it
counties.columns
counties.head(3)
counties.food_env_index.head(3)


# Estimate a model predicting the food environment index,
# based on the share of Black residents, share of Hispanic/Latino residents,
# population, median income, and share of Democrats in 2016
m = sm.formula.ols(
  formula = "food_env_index ~ pop_black + pop_hisplat + pop + median_income", 
  data = counties).fit()


m.summary()


# Let's get a set of hypothetical x values for which to simulate y
# We'll get the medians, but we'll vary the percentage of black residents from 0 to 100%

x = pd.DataFrame({
  'intercept': 1,
  'pop_black': [0, 25, 50, 75, 100],
  'pop_hisplat': counties.pop_hisplat.quantile(q = 0.5),
  'pop': counties['pop'].quantile(q = 0.5),
  'median_income': counties.median_income.quantile(q = 0.5),
})

# View
x




# 1. Prediction #######################################

# First, we'll try a prediction using the build-in functions.

# Generate predictions and return standard errors for each prediction,
p = m.get_prediction(x).summary_frame(alpha = 0.95)


# View it
p

# we care about the columns 'mean', 'mean_se', 'mean_ci_lower', and 'mean_ci_upper'
# These have nothing to do with the mean - they mean prediction


# Let's rename the columns for clarity
qis1 = x
qis1['yhat'] = p['mean']
qis1['se'] = p['mean_se']
qis1['lower'] = p['obs_ci_lower']
qis1['upper'] = p['obs_ci_upper']


# View output
qis1


# Make a data.frame of predicted values, 
# by appending on the fitted/predicted values 
# and the standard errors for each prediction.

# Add lower and upper confidence intervals (technically prediction intervals),
# using the z-value for a 97.5th percentile in a normal distribution as a multiplier
# gives us upper and lower 95% confidence interval

# view it!
qis1


# Visualize it!

# We'll use geom_ribbon() to add a polygon stretching along an x axis from a ymin to a ymax...
# and add a line plot and points afterwards
( ggplot() +
  geom_ribbon(data = qis1, mapping = aes(x = 'pop_black', ymin = 'lower', ymax = 'upper'), 
              fill = "steelblue", alpha = 0.5) +
  geom_line(data = qis1, mapping = aes(x = 'pop_black', y = 'yhat')) +
  geom_point(data = qis1, mapping = aes(x = 'pop_black', y = 'yhat'), size = 3)
)


# Note: in the original video, I evaluated this at levels 0 to 0.25,
# but it really should be the change from 0 to 25, since the % is measured where 1 = 1%.
# So we actually see a very big, statistically significant decline in the food environment index!




# Simulating Marginal Effects ####################################

# We're going to simulate error from a normal distribution,
# using scipy.stats.norm.rvs()
# Here's the basic arguments...
# norm.rvs(loc = mean, scale = sd, size=n)
# Get back 5 values drawn from normal distribution with mean of 3 and sd of 0.5
norm.rvs(loc = 3, scale = 0.5, size = 5)



# Finally, let's estimate the marginal effect 
# of the share of black residents changing from 0 to 25.

# First, we'll get some simulations...
# Get just the two scenarios...
sims = qis1.query('pop_black == 0 or pop_black == 25')

sims

# Add a unique ID
sims['id'] = pd.Series( range(1, len(sims) + 1) ) # throws an error, but works

sims

# For each scenario, simulate error using 1000 simulations
sims = sims.groupby( ['id', 'pop_black'] ).apply(lambda df: pd.Series({
  'yhat': df.yhat.values[0],
  'error': norm.rvs(loc = 0, scale = df.se, size = 1000) 
})).reset_index()

sims

# Pivot the error longer so we have ~5000 simulations
sims = sims.explode('error')

sims

# Add the error to the yhats to get simulated y predictions
sims['ysim'] = sims['yhat'] + sims['error']


# View it!
sims


# Then, let's calculate some simulated differences,
# for each pair of simulations
# Put the scenario simulations side by side...
diffs = pd.DataFrame({
  'y0': sims.query('pop_black == 0').ysim.values,
  'y1': sims.query('pop_black == 25').ysim.values
})

diffs

# Calculate the difference!
diffs['diff'] = diffs['y1'] - diffs['y0']


# Then, let's get some confidence intervals around those differences
effects = pd.DataFrame({
  'estimate': [ diffs['diff'].quantile(q = 0.50) ],
  'lower': [ diffs['diff'].quantile(q = 0.025) ],
  'upper': [ diffs['diff'].quantile(q = 0.975) ]
})


# Show the marginal effect of the share of black residents 
# increasing from 0 to 0.25
# on the predicted change in food index.
effects

# Note: in the original video, I evaluated this at levels 0 to 0.25,
# but it really should be the change from 0 to 25, since the % is measured where 1 = 1%.
# So we actually see a very big, statistically significant decline in the food environment index!


# Cleanup!
globals().clear()
