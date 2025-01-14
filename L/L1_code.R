# L/L1_code.R
# Prediction

# We're going to try to predict food deserts

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

# Load Packages
library(dplyr)
library(readr)
library(broom)
library(ggplot2)

# Load data - county outcomes and traits in 2019
counties = read_csv("L/food_deserts.csv")

counties
counties %>% glimpse()

# Estimate a model predicting the food environment index,
# based on the share of Black residents, share of Hispanic/Latino residents,
# population, median income
m = counties %>%
  lm(formula = food_env_index ~ pop_black + pop_hisplat + pop + median_income) 

m

# Let's get a set of hypothetical x values for which to simulate y
# We'll get the medians, but we'll vary the percentage of black residents from 0 to 100%
x = counties %>%
  reframe(
    intercept = 1,
    pop_black = c(0, 25, 50, 75, 100),
    pop_hisplat = median(pop_hisplat),
    pop = median(pop),
    median_income = median(median_income) )
# View
x



# 1. Prediction #######################################

# First, we'll try a prediction using the build-in functions.

# Generate predictions and return standard errors for each prediction,
p = predict(m, newdata = x, se.fit = TRUE)

# View list output
p

# Make a data.frame of predicted values, 
# by appending on the 'fitted' (predicted) values 
# and the standard errors for each prediction.
qis1 = x %>%  mutate(yhat = p$fit, se = p$se.fit)

# Add lower and upper confidence intervals,
# using the z-value for a 97.5th percentile in a normal distribution as a multiplier
# gives us upper and lower 95% confidence interval
qis1 = qis1 %>%
  mutate(lower = yhat - qnorm(0.975) * se,
         upper = yhat + qnorm(0.975) * se)

# view it!
qis1


# Visualize it!

# We'll use geom_ribbon() to add a polygon stretching along an x axis from a ymin to a ymax...
# and add a line plot and points afterwards
ggplot() +
  geom_ribbon(data = qis1, mapping = aes(x = pop_black, ymin = lower, ymax = upper), 
              fill = "steelblue", alpha = 0.5) +
  geom_line(data = qis1, mapping = aes(x = pop_black, y = yhat)) +
  geom_point(data = qis1, mapping = aes(x = pop_black, y = yhat), size = 3)




# Simulating Marginal Effects ####################################

# Finally, let's estimate the marginal effect 
# of the share of black residents changing from 0 to 0.25.

# get random draws from a normal distribution...
# whose mean is 0...
# and whose standard deviation matches the average prediction error sigma (se)
rnorm(n = 5, mean = 0, sd = 0.0205)

# First, we'll get some simulations...
sims = qis1 %>%
  # Get just the two scenarios...
  filter(pop_black == 0 | pop_black == 25) %>%
  # Add a unique ID
  mutate(id = 1:n()) %>%
  # For each scenario...
  group_by(id, pop_black) %>%
  # simulate error
  reframe(
    yhat = yhat,
    error = rnorm(n = 1000, mean = 0, sd = se),
    ysim = yhat + error
  )

sims

# Then, let's calculate some simulated differences,
# for each pair of simulations
diffs = sims %>%
  reframe(
    y0 = ysim[pop_black == 0],
    y1 = ysim[pop_black == 25],
    diff = y1 - y0
  )

diffs

diffs$diff %>% hist()


# Then, let's get some confidence intervals around those differences
effects = diffs %>%
  reframe(
    lower = quantile(diff, probs = 0.025),
    estimate = quantile(diff, probs = 0.50),
    upper = quantile(diff, probs = 0.975)
  )

# Show the marginal effect of the share of black residents 
# increasing from 0 to 25%
# on the predicted change in food index.
effects

# There is a statistically significant difference in the food environment index
# as the share of black residents changes from 0 to 25%.

# Clean up
rm(list = ls())
