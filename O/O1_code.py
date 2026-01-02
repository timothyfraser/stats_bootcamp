# O1_code.py
# Coding with Probability Distributions
# Tim Fraser

# Getting Started ##########################

# Load packages
import pandas as pd # Import pandas functions
import os
import sys

# We're going to import a bunch of functions 
# written up in the script distributions.py
# This must be in the same folder to work
# This lets us use Python,
# but matches the logic and syntax of R
# Now you can reference them directly
# Append files in this folder (functions) to the Python Path
sys.path.append(os.path.abspath('O'))
# Now you can reference them directly
from distributions import *


# Finding Parameters for Your Distributions #######################

# Let's load in a pandas series of seawall heights in meters.
sw = pd.Series([4.5, 5, 5.5, 5, 5.5, 6.5, 6.5, 6, 5, 4])


# Common Distributions ##############################

## Normal Distributions #########################

# rnorm() can randomly generate for us any numbers randomly sampled from a normal distribution.
# This is a wrapper function, loaded from distributions.py

# For example
mymean = sw.mean()
mysd = sw.std()
# simulate!
mynorm = rnorm(n = 1000, mean = mymean, sd = mysd)
# fun fact: we've written a custom function hist() that does this quickly
hist(mynorm)

# Compare
[mynorm.mean(), mymean]
[mynorm.std(), mysd]
# Pretty close!


## Poisson Distribution ##############################
# Randomly sample from a poisson distribution of counts
# In R the parameter is 'lambda', 
# but in Python, we have to change it to 'mu',
# because lambda is a reserved term.
from scipy

rpois(n=1000, mu = 5).mean()

mypois = rpois(n = 1000, mu = mymean)
hist(mypois)

## Exponential Distribution ######################

# Get lambda, the rate
myrate_e = 1 / sw.mean()
# Simulate
myexp = rexp(n = 1000, rate = myrate_e)
# Visualize!
hist(myexp)
# Compare
[1 / myexp.mean(), myrate_e]
# Pretty close!

## Gamma Distribution ################################

# For shape, we want the rate of how much greater the mean-squared is than the variance.
myshape = sw.mean()**2 / sw.var()

# For rate, we like to get the inverse of the variance divided by the mean.
myrate =  1 / (sw.var() / sw.mean() )

# Simulate it!
mygamma = rgamma(n = 1000, shape = myshape, rate = myrate)

## View it!
hist(mygamma)


## What were the parameter values for this distribution?
[myshape, myrate]

## Weibull Distribution ########################

# Load extra package for fitting distributions
from scipy import stats as fitdistr

# Fit Weibull distribution with location parameter fixed to 0
myshape_w, loc, myscale_w = fitdistr.weibull_min.fit(sw, floc = 0)
# Simulate
myweibull = rweibull(n = 1000, shape = myshape_w, scale = myscale_w)
## View it!
hist(myweibull)


# Special Distributions ##############################

## Binomial Distributions

rbinom(n = 10, size = 1, prob = 0.5)

# In how many cases was the observed value greater than the mean?
myprob = sum(sw > mymean) / len(sw)

# Sample from binomial distribution with that probability
mybinom = rbinom(1000, size = 1, prob = myprob)

# View histogram!
hist(mybinom)



## Uniform Distributions ##########################3

# Simulate a uniform distribution ranging from 0 to 1
myunif = runif(n = 1000, min = 0, max = 1)
# View histogram!
hist(myunif)

# Comparing Distributions #########################



# Finally, we’re going to want to outfit those vectors 
# in nice data.frames (skipping rbinom() and runif()), 
# and stack them into 1 data.frame to visualize.

# Using pandas's concat function...
mysim = pd.concat(
  [
    # Make a bunch of data.frames, all with the same variable names,
    pd.DataFrame({'x': sw, 'type': "Observed"}),
    # and stack them!
    pd.DataFrame({'x': mynorm, 'type': "Normal"}),
    # And stack it!
    pd.DataFrame({'x': mypois, 'type': "Poisson"}),
    # stack, stack, stack stack stack stack stack
    pd.DataFrame({'x': mygamma, 'type': "Gamma"}),
    # so many stacks!
    pd.DataFrame({'x': myexp, 'type': "Exponential"}),
    # so much data!!!!
    pd.DataFrame({'x': myweibull, 'type': "Weibull"})
  ]
)


mysim

# Load plotnine
from plotnine import *

# Let's write the initial graph and save it as an object
g1 = (ggplot(data = mysim, mapping = aes(x = 'x', fill = 'type')) +
  geom_density(alpha = 0.5) +
  labs(x = "Seawall Height (m)", y = "Density (Frequency)", 
       subtitle = "Which distribution fits best?", fill = "Type"))
g1

# Then view it!
g1 + xlim(0,10)


# Yay! Be sure to complete the learning checks to test out your knowledge.
# Great work!

# Clear environment
globals().clear()
