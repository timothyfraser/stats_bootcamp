# E1_code.R
# Sampling and Confidence Intervals

# 0. Getting Started ##########################################################

# Please load our main packages
library(dplyr) # data wrangling
library(readr) # read in data
library(ggplot2) # visualization with ggplot

# Load data
counties <- read_csv("E/environmental_health.csv") %>%
  # Keep just valid air pollution values
  filter(!is.na(air_pollution))

# View first 3 rows of dataset
counties %>% head(3)

# 1. Population Parameters #################################################

# This dataset contains air pollution data for every county in the US, as of 2019.
# counties will be our 'population' dataset, showing the full universe of counties.
pop = counties %>% select(county, fips, air_pollution)

# Let's calculate the mean level of PM 2.5 air pollution,
# in micrograms per cubic meter (PM2.5),
# in an average county,
# based on the entire population of counties.
# We'll name the object 'p' for population, 
# and the statistic 'mu', a Greek letter we use to describe the mean value often.
p = pop %>%
  reframe(mu = mean(air_pollution, na.rm = TRUE))

# View the mean air pollution level
p

# 2. Sample Statistics ###############################################

# But what if we can't measure air pollution in every county? 
# Can we still estimate air pollution from a **sample of counties?**
# Yes - if we take a random sample.

# We can take a random sample of rows from a data.frame like so,
# using sample_n()
sample = pop %>%
  # Sample 100 rows
  sample_n(size = 100) 

# And get the mean
s = sample %>%  
  reframe(mu = mean(air_pollution, na.rm = TRUE))

# Compare the population parameter and the sample statistic.
# Do they differ? A lot?
p
s

# 3. Sampling Distributions #############################################

# We have a rare situation - we actually have the full population.
# We can **prove** that this random sample should generally work.

# We can repeatedly take samples from this population,
# calculate statistics from each, 
# and view the distribution of statistics.
# That distribution is called a sampling distribution.

# It shows how much a statistic varies due to random sampling / chance.
d = tibble(rep = 1:1000) %>%
  group_by(rep) %>%
  reframe(pop %>% sample_n(size = 100)) %>%
  group_by(rep) %>%
  summarize(mu = mean(air_pollution, na.rm = TRUE))
# Let's view 'd', our sampling distribution data.frame
d

# Let's view the histogram of this vector of statistics.
d$mu %>% hist()


# Whoa! It's normally distributed!
# And the values aren't totally random - 
# they cluster around the true population parameter!



# 4. Confidence Intervals #######################################################

# Because of sampling, **every statistic** has error,
# so we should probably be able to measure and communicate that error to our users.
# Our sampling distribution 'd' shows that error.
# How might we describe it?

# the middle-most estimate of the mean is the median statistic
d %>%
  reframe(median = quantile(mu, probs = 0.50))

# 50% of the time, the statistic would range from [lower] to [upper]
d %>% 
  reframe(lower = quantile(mu, probs = 0.25),
          upper = quantile(mu, probs = 0.75))

# 95% of the time, the statistic would range from [lower] to [upper]
d %>% 
  reframe(lower = quantile(mu, probs = 0.025),
          upper = quantile(mu, probs = 0.975))

# This is your 95% confidence interval!

# We can state it like so:

# 'Even if our statistic was off due to random sampling error,
# 95% of the time the statistic would range from [A] to [B]'

# OR:

# The mean air pollution level was XXX,
# with a 95% confidence interval ranging from AAA to BBB.


# 5. Standard Errors ##############################################################

# But in reality, we NEVER get to see the full population,
# so we can never make the full sampling distribution.

# But what if we could approximate it???

# Mathematicians have devise that the 'standard error' (sd / sqrt(n))
# very closely approximates the standard deviation of a sampling distribution.

sample %>%
  summarize(sd = sd(air_pollution, na.rm = TRUE),
            n = n(),
            se = sd / sqrt(n))

# Let's compare that to the standard deviation of the sampling distribution!
sd(d$mu) 


# HOLY CRAP! It works!

# 6. Confidence Intervals with Normal Distribution Approximation ##############################

# In a normal distribution with a mean of 0 and standard deviation of 1,
# the 97.5th percentile is about ~2 standard deviations from the mean.

# We can check this with the qnorm() function.
qnorm(0.975)

# This multiplier (called 'z') can be paired with our standard error
# to approximate confidence intervals


stat = sample %>%
  reframe(
    mu = mean(air_pollution, na.rm = TRUE),
    sd = sd(air_pollution, na.rm = TRUE),
    n = n(),
    se = sd / sqrt(n),
    # Estimate the confidence interval!
    z = qnorm(0.975),
    lower = mu - se * z,
    upper = mu + se * z
  )

# View our statistics!
stat

# How does that compare to our true sampling distribution again?

d %>% 
  reframe(lower = quantile(mu, probs = 0.025),
          upper = quantile(mu, probs = 0.975))

# Pretty close!





# 7. Bootstrapping the Sampling Distribution ######################################


# But in reality, we NEVER get to see the full population,
# so we can never make the full sampling distribution.

# But what if we could approximate it,
# *without* assuming a normally distributed sampling distribution?

# Using bootstrapping (aka sampling with replacement),
# we can approximate what the sampling distribution would look like.

# This is because we're injecting random sampling error into our sample,
# by resampling with replacement from our sample, 
# creating slightly different samples many many times in a row

# 1000 times in a row...
b = tibble(rep = 1:1000) %>%
  # For each time...
  group_by(rep) %>%
  # Take a random sample with replacement of 100 rows from the sample itself
  reframe(
    sample %>% sample_n(size = 100, replace = TRUE)
  ) %>%
  # Now for each sample...
  group_by(rep) %>%
  # Calculate the mean
  summarize(mu = mean(air_pollution, na.rm = TRUE))

# View the distribution!
b$mu %>% hist()

# This is an approximated sampling distribution,
# also known as a bootstrapped sampling distribution.



# 8. Comparisons ######################################################


# How do these estimates compare?

ggplot() +
  geom_histogram(data = d, mapping = aes(x = mu, fill = "Sampling\nDistribution"), alpha = 0.5) +
  geom_vline(mapping = aes(xintercept = p$mu, color = "Population Mean")) +
  geom_histogram(data = b, mapping = aes(x = mu, fill = "Bootstrapped\nSampling\nDistribution"), alpha = 0.5) +
  geom_vline(mapping = aes(xintercept = s$mu, color = "Sample Mean"))

# Let's compare the standard error of the sampling distribution vs. the bootstrapped sampling distribution,
# by taking the standard deviation of each.

sd(d$mu)
sd(b$mu)

# Very close!!!
# Interesting that even if the sample mean deviations from the population mean,
# the standard error remains pretty darn close.

# No sample is ever going to be a perfect representation of the population.
# There will ALWAYS be error.
# But by taking random samples, we ensure the error will be RANDOM.


# Cleanup ###############################################################

# Clean our environment!
rm(list = ls())




