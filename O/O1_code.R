# O1_code.R
# Coding with Probability Distributions
# Tim Fraser

# Getting Started ##########################

# Load packages
library(dplyr)   # for dplyr functions
library(ggplot2) # for ggplot2

# Seawall heights data
sw = c(4.5, 5, 5.5, 5, 5.5, 6.5, 6.5, 6, 5, 4)

# Common Distributions ##############################

## Normal Distributions #########################

# rnorm() can randomly generate for us any numbers randomly sampled from a normal distribution.
# For example
mymean = mean(sw)  # Calculate the mean of seawall heights
mysd = sd(sw)      # Calculate the standard deviation of seawall heights

# Simulate normal distribution
mynorm = rnorm(1000, mean = mymean, sd = mysd)

# Compare mean and sd
c(mean(mynorm), mymean)  # Should be close
c(sd(mynorm), mysd)      # Should be close

# Visualize the normal distribution
hist(mynorm)

## Poisson Distribution ##############################

# In R the parameter is 'lambda', but in Python, we have to change it to 'mu',
# because lambda is a reserved term in Python.
# Simulate Poisson distribution
mypois = rpois(1000, lambda = mymean)

# Visualize Poisson distribution
hist(mypois)

## Exponential Distribution ######################

# Get lambda (rate) from the mean of the seawall heights
myrate_e = 1 / mean(sw)

# Simulate exponential distribution
myexp = rexp(1000, rate = myrate_e)

# Compare means of the simulated and expected values
c(1 / mean(myexp), myrate_e)

# Visualize the exponential distribution
hist(myexp)

## Gamma Distribution ################################

# For shape, we want the rate of how much greater the mean-squared is than the variance.
myshape = mean(sw)^2 / var(sw)

# For rate, we like to get the inverse of the variance divided by the mean.
myrate = 1 / (var(sw) / mean(sw))

# Simulate Gamma distribution
mygamma = rgamma(1000, shape = myshape, rate = myrate)

# Visualize Gamma distribution
hist(mygamma)

# What were the parameter values for this distribution?
c(myshape, myrate)


## Weibull Distribution ########################

# Fit Weibull distribution with location parameter fixed to 0

fit_weibull = MASS::fitdistr(sw, densfun = "weibull")
myshape_w = fit_weibull$estimate["shape"]
myscale_w = fit_weibull$estimate["scale"]

# Simulate Weibull distribution
myweibull = rweibull(1000, shape = myshape_w, scale = myscale_w)

# Visualize Weibull distribution
hist(myweibull)



# Special Distributions ##############################

## Binomial Distributions ########################

# Simulate binomial distribution with size = 1, prob = 0.5
mybinom = rbinom(1000, size = 1, prob = 0.5)

# In how many cases was the observed value greater than the mean?
myprob = mean(sw > mymean)

# Sample from binomial distribution with the calculated probability
mybinom_obs = rbinom(1000, size = 1, prob = myprob)

# Visualize the binomial distribution
hist(mybinom_obs)

## Uniform Distributions ##########################

# Simulate uniform distribution ranging from 0 to 1
myunif = runif(1000, min = 0, max = 1)

# Visualize uniform distribution
hist(myunif)

# Combining distributions #########################

# Create a tidy data frame to store and stack the distributions
mysim = bind_rows(
  data.frame(x = sw, type = "Observed"),  # Observed data
  data.frame(x = mynorm, type = "Normal"),  # Normal distribution
  data.frame(x = mypois, type = "Poisson"),  # Poisson distribution
  data.frame(x = mygamma, type = "Gamma"),  # Gamma distribution
  data.frame(x = myexp, type = "Exponential"),  # Exponential distribution
  data.frame(x = myweibull, type = "Weibull")  # Weibull distribution
)


# Plot using ggplot2
library(ggplot2)
g1 = ggplot(data = mysim, aes(x = x, fill = type)) +
  geom_density(alpha = 0.5) +  # Density plot with transparency
  labs(x = "Seawall Height (m)", y = "Density (Frequency)", 
       subtitle = "Which distribution fits best?", fill = "Type")

# View plot
print(g1 + xlim(0, 10))  # Limiting x-axis to the range 0 to 10

# Clear environment
rm(list = ls())

