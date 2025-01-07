# E1_code.R
# Sampling and Confidence Intervals

# 0. Getting Started ##########################################################

# Please load our main packages
import pandas as pd # data wrangling
from plotnine import * # data visualization
import scipy # probability functions

# Load data
counties = pd.read_csv("E/environmental_health.csv").dropna()
# Keep just valid air pollution values

# View first 3 rows of dataset
counties.head(3) 



# 1. Population Parameters #################################################

# This dataset contains air pollution data for every county in the US, as of 2019.
# counties will be our 'population' dataset, showing the full universe of counties.
pop = counties[ ["county", "fips", "air_pollution"] ]


# Let's calculate the mean level of PM 2.5 air pollution,
# in micrograms per cubic meter (PM2.5),
# in an average county,
# based on the entire population of counties.
# We'll name the object 'p' for population, 
# and the statistic 'mu', a Greek letter we use to describe the mean value often.

p = pd.DataFrame({'mu': pd.Series( pop.air_pollution.mean() ) })


# View the mean air pollution level
p




# 2. Sample Statistics ###############################################

# But what if we can't measure air pollution in every county? 
# Can we still estimate air pollution from a **sample of counties?**
# Yes - if we take a random sample.

# We can take a random sample of rows from a data.frame like so,
# using sample()

# Sample 100 rows
sample = pop.sample(n = 100)
sample

# And get the mean
s = pd.DataFrame({'mu': pd.Series( sample.air_pollution.mean() ) })


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
d = pd.DataFrame({ 
    'rep': range(1,1000+1)  
    # For each rep, apply this function...
  }).groupby('rep').apply(
    # Where df is that rep...
    lambda df: pd.Series({
  'mu': pop.sample(n = 100).air_pollution.mean()
  })
  # Then return 'rep' to be a column
).reset_index()

# Let's view 'd', our sampling distribution data.frame
d

# Let's view the histogram of this vector of statistics.
( ggplot() + geom_histogram(data = d, mapping = aes(x = 'mu')) )



# Whoa! It's normally distributed!
# And the values aren't totally random - 
# they cluster around the true population parameter!



# 4. Confidence Intervals #######################################################

# Because of sampling, **every statistic** has error,
# so we should probably be able to measure and communicate that error to our users.
# Our sampling distribution 'd' shows that error.
# How might we describe it?

# the middle-most estimate of the mean is the median statistic
d.mu.quantile(q = 0.50)

# 50% of the time, the statistic would range from [lower] to [upper]
d.mu.quantile(q = [0.25, 0.75])


# 95% of the time, the statistic would range from [lower] to [upper]
d.mu.quantile(q = [0.025, 0.975])


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

pd.DataFrame({
  'sd': [ sample.air_pollution.std() ],
  'n': [ len( sample.air_pollution.dropna() ) ],
  'se': [ sample.air_pollution.std()  / len( sample.air_pollution.dropna() )**0.5 ]
})


# Let's compare that to the standard deviation of the sampling distribution!
d.mu.std()



# HOLY CRAP! It works!





# 6. Confidence Intervals with Normal Distribution Approximation ##############################

# In a normal distribution with a mean of 0 and standard deviation of 1,
# the 97.5th percentile is about ~2 standard deviations from the mean.

# We can check this with the norm.ppf() function from the scipy package
scipy.stats.norm.ppf(0.975)

# This multiplier (called 'z') can be paired with our standard error
# to approximate confidence intervals


stat = pd.DataFrame({
  'mu': [ sample.air_pollution.mean() ],
  'sd': [ sample.air_pollution.std() ],
  'n': [ len( sample.air_pollution.dropna() ) ],
  'se': [ sample.air_pollution.std()  / len( sample.air_pollution.dropna() )**0.5 ],
  'z': [ scipy.stats.norm.ppf(0.975) ]
})
# Calculate confidence interval by taking z standard errors above / below mean
stat['lower'] = stat.mu - stat.se * stat.z
stat['upper'] = stat.mu + stat.se * stat.z


# View our statistics!
stat

# How does that compare to our true sampling distribution again?
d.mu.quantile(q = [0.025, 0.975])


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
b = pd.DataFrame({ 
    'rep': range(1,1000+1)  
    # For each rep, apply this function...
  }).groupby('rep').apply(
    # Where df is that rep...
    lambda df: pd.Series({
      # Sample with replacement, then calculate the mean
      'mu': pop.sample(n = 100, replace = True).air_pollution.mean()
  })
  # Then return 'rep' to be a column
).reset_index()

# View the distribution!
( ggplot() + geom_histogram(data = b, mapping = aes(x = 'mu')) )

# This is an approximated sampling distribution,
# also known as a bootstrapped sampling distribution.



# 8. Comparisons ######################################################


# How do these estimates compare?

# Make a data.frame to house the distributions,
# labeling and stacking them
p['type'] = "Population Mean"
s['type'] = "Sample Mean"
lines = pd.concat([p, s])

# Make a data.frame to house the distributions, 
# labeling and stacking them atop each other with pd.concat()
d['type'] = "Sampling\nDistribution"
b['type'] = "Bootstrapped\nSampling\nDistribution"
dists = pd.concat([b,d])


# Now visualize them, split by type;
# (use position = 'identity' to make sure the histograms overlap, not stack)
( ggplot() +
  # plot histograms
  geom_histogram(data = dists, mapping = aes(x = 'mu', fill = 'type'), alpha = 0.5, position = 'identity') +
  # plot vertical lines...
  geom_vline(data = lines, mapping = aes(xintercept = 'mu', color = 'type')) )

# Pretty darn close overlap.

# Let's compare the standard error of the sampling distribution vs. the bootstrapped sampling distribution,
# by taking the standard deviation of each.

d.mu.std()
b.mu.std()

# Very close!!!
# Interesting that even if the sample mean deviations from the population mean,
# the standard error remains pretty darn close.

# No sample is ever going to be a perfect representation of the population.
# There will ALWAYS be error.
# But by taking random samples, we ensure the error will be RANDOM.


# Cleanup ###############################################################

# Clean our environment!
globals().clear()




