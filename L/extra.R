# L/extra.R
# Extra material for those interested, in R

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

# Make sure you have installed the MASS package.
# install.packages("MASS")

# Load Packages
library(dplyr)
library(readr)
library(broom)
library(ggplot2)

# Load data - county outcomes and traits in 2019
counties = read_csv("L/food_deserts.csv")

counties %>% glimpse()

# Estimate a model predicting the food environment index,
# based on the share of Black residents, share of Hispanic/Latino residents,
# population, median income, and share of Democrats in 2016
m = counties %>%
  lm(formula = food_env_index ~ pop_black + pop_hisplat + pop + median_income) 


# Let's get a set of hypothetical x values for which to simulate y
# We'll get the medians, but we'll vary the percentage of black residents from 0 to 100%
x = counties %>%
  reframe(
    intercept = 1,
    pop_black = c(0, 0.25, 0.50, 0.75, 1),
    pop_hisplat = median(pop_hisplat),
    pop = median(pop),
    median_income = median(median_income) )
# View
x

# 1. Prediction #######################################

# First, we'll try a prediction using the build-in functions.

# Generate predictions and return standard errors for each prediction,
p = predict(m, newdata = x, se.fit = TRUE)
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


# 2. Fundamental Uncertainty ###########################################

# Sometimes we may want to simulate error 
# by taking random draws from a normal distribution
# because normal methods might not work.

sigma = glance(m)$sigma # get root mean squared error 

# We could take the 'sigma' statistic - the residual standard error,
# aka the average prediction error,
# and randomly add error to each of our predictions
# by drawing from a normal distribution
# whose width matches that distribution.

pred2 =  x %>%
  # Make prediction and get residual standard error sigma
  mutate(yhat = predict(m, newdata = .),
         se = glance(m)$sigma) %>%
  # Add a unique id per row.
  mutate(id = 1:n())

# Next, let's simulate for each row/group...
sims2 = pred2 %>%
  group_by(id, pop_black) %>%
  reframe(
    ysim = yhat + rnorm(n = 1000, mean = 0, sd = sigma)
  ) 
# View it!
sims2

# For each group, let's get quantities of interest,
# eg. confidence intervals
qis2 = sims2 %>% 
  group_by(id, pop_black) %>%
  reframe(lower = quantile(ysim, probs = 0.025),
          median = quantile(ysim, probs = 0.50),
          upper = quantile(ysim, probs = 0.975))

# View our quantities of interest!
qis2


# Visualize our quantities of interest!
# and add a line plot and points afterwards
ggplot() +
  geom_ribbon(data = qis2, mapping = aes(x = pop_black, ymin = lower, ymax = upper), 
              fill = "steelblue", alpha = 0.5) +
  geom_line(data = qis2, mapping = aes(x = pop_black, y = median)) +
  geom_point(data = qis2, mapping = aes(x = pop_black, y = median), size = 3)


# 3. Simulating Estimation Uncertainty ###############################

# Alternatively, we could try an even more robust form of simulation,
# where we account for estimation uncertainty,
# We simulate estimation uncertainty by varying our beta coefficients,


# Extract some ingredients for simulation
mu = m$coefficients # get alpha/beta coefficients
vcov = vcov(m) # get variance covariance matrix
sigma = glance(m)$sigma # get root mean squared error 


# Make just 1 sample...
MASS::mvrnorm(n = 1, mu = mu, Sigma = vcov)
# Compare against our observed coefficients mu
mu
# They're different!

# Let's get 1000 simulated coefficients
sims3 = data.frame(MASS::mvrnorm(n = 1000, mu = mu, Sigma = vcov)) %>%
  rename(intercept = 1) # give the intercept a readable name

head(sims3, 5) # view them!


# For each predictor value of x,
# we're going to calculate a simulated y-predicted value,
# by computing the model equation with the new varied beta coefficients
sims3 = x %>%
  mutate(id = 1:n()) %>%
  group_by(id, pop_black) %>%
  reframe(
    ysim = intercept * sims3$intercept + 
      pop_black * sims3$pop_black +
      pop_hisplat * sims3$pop_hisplat +
      pop * sims3$pop +
      median_income * sims3$median_income
  )

# View our estimates!
sims3

# Estimate quantities of interest, having accounted for estimation uncertainty.
qis3 = sims3 %>% 
  group_by(id, pop_black) %>%
  reframe(lower = quantile(ysim, probs = 0.025),
          median = quantile(ysim, probs = 0.50),
          upper = quantile(ysim, probs = 0.975))

# View our quantities of interest!
qis3


# Visualize our quantities of interest!
# and add a line plot and points afterwards
ggplot() +
  geom_ribbon(data = qis3, mapping = aes(x = pop_black, ymin = lower, ymax = upper), 
              fill = "steelblue", alpha = 0.5) +
  geom_line(data = qis3, mapping = aes(x = pop_black, y = median)) +
  geom_point(data = qis3, mapping = aes(x = pop_black, y = median), size = 3)


# 4. Estimation and Fundamental Uncertainty ##############################

# Alternatively, we could try an even more robust form of simulation,
# where we account for MULTIPLE types of uncertainty.
# We simulate estimation uncertainty by varying our beta coefficients,
# and then
# we simulate fundamental uncertainty by varying the resulting predictions.


# Extract some ingredients for simulation
mu = m$coefficients # get alpha/beta coefficients
vcov = vcov(m) # get variance covariance matrix
sigma = glance(m)$sigma # get root mean squared error 


# Let's get 1000 simulated coefficients
sims4 = data.frame(MASS::mvrnorm(n = 1000, mu = mu, Sigma = vcov)) %>%
  rename(intercept = 1) # give the intercept a readable name

# Let's compute the model equations for each to get predictions, like before,
# incorporating estimation uncertainty.
sims4 = x %>%
  mutate(id = 1:n()) %>%
  group_by(id, pop_black) %>%
  reframe(
    ysim = intercept * sims4$intercept + 
      pop_black * sims4$pop_black +
      pop_hisplat * sims4$pop_hisplat +
      pop * sims4$pop +
      median_income * sims4$median_income
  )

# Let's account for fundamental uncertainty!
# For each simulation, we'll now vary it slightly using random draws 
# from a normal distribution with a standard deviation matching the residual standard error
pvs = sims4 %>%
  group_by(id, pop_black) %>%
  reframe(
    ysim = ysim + rnorm(n = n(), mean = 0, sd = sigma)
  )

# Take these predicted values and get quantities of interest.
qis4 = pvs %>%
  group_by(id, pop_black) %>%
  reframe(lower = quantile(ysim, probs = 0.025),
          median = quantile(ysim, probs = 0.50),
          upper = quantile(ysim, probs = 0.975))
qis4


# COMPARE ############################################

# Let's end by comparing these predictions.

viz = bind_rows(
  qis1 %>% mutate(type = "Prediction\n\n") %>% 
    select(estimate = yhat, lower, upper, type, pop_black),
  qis2 %>% mutate(type = "Simulated\nFundamental\nUncertainty\n") %>% 
    select(estimate = median, lower, upper, type, pop_black),
  qis3 %>% mutate(type = "Simulated\nEstimation\nUncertainty\n") %>%
    select(estimate = median, lower, upper, type, pop_black),
  qis4 %>% mutate(type = "Simulated\nEstimation &\nFundamental\nUncertainty\n") %>%
    select(estimate = median, lower, upper, type, pop_black)
)

viz

# view it!
ggplot() +
  geom_ribbon(
    data = viz, 
    mapping = aes(x = pop_black, ymin = lower, ymax = upper, 
                  group = type, fill = type), 
    alpha = 0.5)


rm(list = ls())


