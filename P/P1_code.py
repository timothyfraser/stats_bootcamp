# P1_code.py
# Exercise: Maximum Likelihood Estimation
# Prof. Tim Fraser

# This tutorial will introduce you to Fitting Distribution Parameters in Python, 
# teaching you how to use distribution fitting functions from the scipy.stats 
# package in Python.
#
# This training continues on our previous work on Descriptive Statistics. 
# Often, we might want to approximate statistics describing the shape of 
# distributions, but there may not be a clear analytical method (eg. method 
# of moments) to do so. We can use the power of optimization to help us 
# instead, using a brute-force method to find the value most likely to be the 
# statistic that actually fits our distribution. We can ask Python to compute the 
# values of those statistics using the scipy.stats package's distribution 
# fitting methods.
#
# Please open up your project on Posit.Cloud, for our Github class repository
# (https://github.com/timothyfraser/sysen). Start a new Python script 
# (File >> New >> Python Script). Save the Python script as P1_code.py. 
# And let's get started!

# !pip install scipy numpy pandas matplotlib


# 1. Getting Started #######################################

# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import minimize, minimize_scalar

# As our raw data, let's use our vector of seawall heights sw. 
# Its raw distribution can be visualized with hist(sw).

# Let's remake again our vector of seawall heights
sw = [4.5, 5, 5.5, 5, 5.5, 6.5, 6.5, 6, 5, 4]
plt.hist(sw)
plt.show()


# 2. Example: Exponential Distribution #######################################

# We have our vector of seawall heights sw. We have 2 main ways of 
# calculating statistics that describe the distribution of sw. These include 
# an analytical approach (method of moments) and a brute-force approach 
# (maximum likelihood estimation).
#
# - In the analytical approach (method of moments), 
#   we may use formula that have been derived by mathematicians to 
#   describe the parameters of a particular distribution.
#
# - In the brute-force approach (maximum likelihood estimation), we use a 
#   secondary parameter called likelihood to find the parameter values most 
#   likely to fit your data. We say, if the parameter had value A (for 
#   example), what's the joint probability (likelihood) of finding your 
#   observed values (sw) in a distribution with that trait A? We use maximum 
#   likelihood estimation to iteratively test various different values for 
#   parameter A, and choose the value that provides the highest likelihood - 
#   a.k.a. the maximum likelihood.
#
# Note: Remember: a parameter is a single number that describes a full 
# population. A statistic is a single number that describes a sample. This 
# key difference aside, the terms are largely interchangeable.
#
# Let's use the exponential distribution as a helpful example. It has one 
# parameter - rate (also known as lambda), describing 1/mean.
#
# Let's calculate the rate parameter a few ways, using (1) the method of 
# moments, (2) maximum likelihood estimation (MLE) using scipy.stats.expon.fit(), 
# and (3) maximum likelihood estimation (MLE) using scipy.optimize.


# 2.1. Method of Moments #######################################

# Let's use the method of moments to find the inverse mean
1 / (sum(sw) / len(sw))
# Equivalent to...
1 / np.mean(sw)


# 2.2. MLE with scipy.stats.expon.fit() #######################################

# Let's ask scipy.stats.expon.fit() to run maximum likelihood estimation.
#
# Maximum likelihood estimation requires a benchmark distribution to compare 
# against, so we need to specify the distribution type. In this case, let's do 
# exponential. (See scipy.stats documentation for other supported distributions)

# Note: scipy.stats.expon.fit() returns parameters in a different format than R's fitdistr
# For exponential, it returns (loc, scale) where scale = 1/rate
# We'll extract the scale parameter and convert to rate

params = stats.expon.fit(sw, floc=0)  # floc=0 fixes location at 0
rate_estimate = 1 / params[1]  # params[1] is the scale parameter
print(f"Rate parameter (lambda): {rate_estimate}")
print(f"Full parameters (loc, scale): {params}")

# Pretty darn similar to the value we got from the method of moments, right?


# 2.3. MLE with scipy.optimize #######################################

# Alternatively, we could run maximum likelihood estimation manually, using 
# scipy.optimize. scipy.optimize is Python's built in optimization function. 
# The key idea is this:
#
# stats.expon.pdf(x = 2, scale = 1/0.1) gives the probability of the value 
# x = 2 showing up in an exponential distribution characterized by a parameter 
# rate = 0.1 (where scale = 1/rate).

stats.expon.pdf(2, scale=1/0.1)

# stats.expon.pdf(x = sw, scale = 1/0.1) gives the probabilities for each value 
# of x if they showed up in an exponential distribution characterized by a 
# parameter rate = 0.1.

# You can compute the probabilities for all values in sw like this
stats.expon.pdf(sw, scale=1/0.1)

# The joint probability of these values of x occurring together is called the 
# likelihood. We can take the product using np.prod().

# Let's get the likelihood of these values...
np.prod(stats.expon.pdf(sw, scale=1/0.1))

# Likelihood tend to be very small numbers, so a helpful trick is to calculate 
# the log-likelihood instead, meaning the sum of logged probabilities.

# See how these two processes produce the same output?
# Get the log of probabilities multiplied together...
np.log(np.prod(stats.expon.pdf(sw, scale=1/0.1)))

# Get the sum of logged probabilities...
np.sum(np.log(stats.expon.pdf(sw, scale=1/0.1)))

# They're equivalent

# Then, we write up a short function called loglikelihood(), including two 
# inputs (1) par and (2) our data x. I added an example value 0.1 to par just 
# as a reminder for what it means.

def loglikelihood(par, x):
    # par is the rate parameter, scale = 1/par
    return np.sum(np.log(stats.expon.pdf(x, scale=1/par)))

# Try it!
loglikelihood(0.1, sw)
loglikelihood(0.15, sw)
loglikelihood(0.18, sw)
loglikelihood(0.2, sw)
loglikelihood(0.25, sw)
loglikelihood(0.3, sw)

# Finally, we run an optimizer using minimize_scalar(), supplying a starting 
# value for search and our function loglikelihood. We want to maximize the 
# loglikelihood, but minimize_scalar() minimizes by default, so we'll use 
# method='brent' and negate our function to maximize it.

# Note: We need to minimize the negative log-likelihood to maximize the log-likelihood
result = minimize_scalar(lambda par: -loglikelihood(par, sw), 
                         bounds=(0.001, 10), 
                         method='bounded')
print(result)

# Compare the final parameter value against scipy.stats.expon.fit()'s results! 
# They're about the same.

params = stats.expon.fit(sw, floc=0)
rate_estimate = 1 / params[1]
print(f"Rate parameter from fit(): {rate_estimate}")

# Voila! You made your own maximum likelihood estimator manually. Certainly, 
# scipy.optimize was a little more time consuming, but now you know how 
# distribution fitting truly works inside!


# 3. Applications #######################################

# Let's try applying the same general approach with scipy.stats to other 
# distributions.


# 3.1. Normal Distribution #######################################

# What parameter values would best describe our distribution's shape, if this 
# data were from a normal distribution? Remember, normal distributions have 
# a mean and a sd.

# Method of Moments
np.mean(sw)
np.std(sw, ddof=1)  # ddof=1 for sample standard deviation
# Maximum Likelihood Estimation
# stats.norm.fit() returns (loc, scale) where loc=mean and scale=std
params_norm = stats.norm.fit(sw)
print(f"Normal distribution parameters (mean, std): {params_norm}")


# 3.2. Gamma Distribution #######################################

# What parameter values would best describe our distribution's shape, if this 
# data were from a Gamma distribution? Remember, gamma distributions have a 
# shape parameter approximately equal to mean^2/variance and a scale parameter 
# approximately equal to variance/mean.

# Method of Moments
# For shape, we want the rate of how much greater the mean-squared is than 
# the variance.
np.mean(sw)**2 / np.var(sw, ddof=1)

# For scale, we like to get the variance divided by the mean.
np.var(sw, ddof=1) / np.mean(sw)

# Maximum Likelihood Estimation
# stats.gamma.fit() returns (a, loc, scale) where a is the shape parameter
params_gamma = stats.gamma.fit(sw, floc=0)
print(f"Gamma distribution parameters (shape, scale): ({params_gamma[0]}, {params_gamma[2]})")


# 3.3. Weibull Distribution #######################################

# What parameter values would best describe our distribution's shape, if this 
# data were from a Weibull distribution? Remember, weibull distributions have 
# a shape parameter and a scale parameter. (But we can't easily use the method 
# of moments here right now.)

# Estimate the shape and scale parameters for a weibull distribution
# stats.weibull_min.fit() returns (c, loc, scale) where c is the shape parameter
params_weibull = stats.weibull_min.fit(sw, floc=0)
print(f"Weibull distribution parameters (shape, scale): ({params_weibull[0]}, {params_weibull[2]})")


# 4. Learning Check 1 #######################################

# Question:
#
# You've been recruited to evaluate the frequency of Corgi sightings in the 
# Ithaca Downtown. A sample of 10 students each reported the number of corgis 
# they saw last Tuesday in town. Calculate the statistics summarizing each 
# distribution, if it were a normal, poisson, exponential, gamma, or weibull 
# distribution. Please use scipy.stats distribution fitting methods for all 
# your calculations.
#
# Beth saw 5, Javier saw 1, June saw 10(!), Tim saw 3, Melanie saw 4, 
# Mohammad saw 3, Jenny say 6, Yosuke saw 4, Jimena saw 5, and David saw 2.
#
# ----------------------------------------------------------------------------
# View Answer!
# ----------------------------------------------------------------------------

# First, let's make the data.

# Make distribution of Corgis
corgi = [5, 1, 10, 3, 4, 3, 6, 4, 5, 2]

# Next, let's compute the estimated statistics using maximum likelihood 
# estimation.

# Compute statistics for each distributions
print("Normal distribution:")
print(stats.norm.fit(corgi))
print("\nExponential distribution:")
exp_params = stats.expon.fit(corgi, floc=0)
print(f"Rate (lambda): {1/exp_params[1]}")
print("\nGamma distribution:")
gamma_params = stats.gamma.fit(corgi, floc=0)
print(f"Shape: {gamma_params[0]}, Scale: {gamma_params[2]}")
print("\nWeibull distribution:")
weibull_params = stats.weibull_min.fit(corgi, floc=0)
print(f"Shape: {weibull_params[0]}, Scale: {weibull_params[2]}")


# 5. Conclusion #######################################

# Congratulations! You now know how to use scipy.stats distribution fitting 
# methods to approximate the parameters for a dataset, assuming various 
# different types of distributions. You also learned maximum likelihood 
# estimation, the core technique underneath these fitting methods, and how to 
# perform it manually using scipy.optimize. Great work!

# Clean up workspace (optional)
# Note: In Python, you can use del to remove variables, or just restart the kernel
globals().clear()
