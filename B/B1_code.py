# Training: Descriptive Statistics
# Tim Fraser


# This tutorial will introduce you to how to code
# and analyze distributions in Python using descriptive statistics.

# Getting Started ##########################

# Please open up this script in your preferred computing environment;
# I recommend a Posit.Cloud project or (for Python only) Google Colabs.

# Load packages
import pandas as pd # Import pandas functions


# Our Data ####################


# You could code it as a vector, save it as an object, then use your functions!
sw = pd.Series([4.5, 5, 5.5, 5, 5.5, 6.5, 6.5, 6, 5, 4])
# View it
sw


# Any vector can be expressed as a distribution
# (especially numeric vectors). 
# A distribution stacks the values in a vector in order
# from lowest to highest to show the frequency of values.
# There are several ways to visualize distributions, 
# including histograms, density plots, violin plots, 
# jitter plots, ribbon plots, and more; 
# the most common are histograms and density plots.


# What’s a statistic? A statistic is a single number
# that summarizes something about a sample. 
# That’s it! No magic!
# Statistics is the process of making statistics
# (eg. many single numbers) so we can understand samples of data! 
# They help people make decisions when faced with uncertainty.
# We’ll learn several functions to make statistics that
# describe our distributions.

# Any distribution can be described with 4 traits.
# These include: 
# - Size (how many values are in it), 
# - Location (eg. where is it clumped), 
# - Spread (how much do values vary?), and; 
# - Shape (eg. bell curve).



# Size ########################

## Length ##########################

# How big is our sample?
len(sw)



# Location #######################

# Where is our sample clustered? 
# What is the central tendency / most central values
# of the distribution?


## Mean #######################
sw.mean()
## Median ########################
sw.median()
## Mode ########################
sw.mode()




# Spread (1) ###########################

# Spread: How much does our sample vary?


# What are the most extreme values?
# Percentiles
sw.quantile(q = 0) # min
sw.quantile(q = 1) # max

sw.min()
sw.max()
sw.quantile(q = .50)


# Where do the middle-most 50% of values lie?
sw.quantile(q = .25) # 25th percentile
sw.quantile(q = .75) # 75th percentile




# Spread (2) ##########################

## Standard Deviation #####################

# But we can also evaluate how much our values vary 
# from the mean on average -
# the standard deviation, often abbreviated as  
# σ (sigma)

x = (sw - sw.mean())**2 # get squared deviations from mean
x = x.sum() # get sum
x = x / (len(sw) - 1) # divide by length - 1
x = x**0.5 # square root

x # view it

# Or, much more quickly...
sw.std()

# Remove x
del x



## Variance ########################

# Sometimes, we might want the variance,
# which is the standard deviation squared.
# This accentuates large deviations in a sample.

sw.var()

sw.std()**2 # same!



## Coefficient of Variation (CV) ###############

# We could also calculate the coefficient of variation (CV),
# meaning how great a share of the mean
# does that average variation constitute?
# (Also put, how many times does the mean fit 
# into the standard deviation.)



# How many times does the mean fit into the standard deviation?
# How great a share of the mean does that average variation constitute?
sw.std() / sw.mean()

# The standard deviation constitutes 15% of the 
# size of the mean seawall height.


## Standard Error (SE) ###########################

# But these numbers don’t have much meaning to us, 
# unless we know seawalls really well. 
# Wouldn’t it be nice if we had a kind of uniform measure, 
# that told us how big is the variation in the data, 
# given how big the data is itself?

# Good news! We do! 

# How big is the variation in the data, given how big the data sample size is?


# sample size adjusted variance
sw.var() / len(sw)

# This means we could take this set of seawalls and
# compare it against samples of coastal infrastructure in Louisiana,
# in Japan, in Australia, and make meaningful comparisons,
# having adjusted for sample size.

# However, sample-size adjusted variance is a little bit
# of a funky concept, and so it’s much more common for us
# to use the sample-size adjusted standard deviation, 
# more commonly known as the standard error, or se.

# standard error = sample size adjusted standard deviation
# Calculated as 
se = sw.std() / (len(sw)**0.5)
se 
# Or as:
(sw.std()**2 / len(sw) )**0.5
# Or as
(sw.var() / len(sw))**0.5




# Shape #############################

# How then do we describe the shape of a distribution? 
# We can use skewness and kurtosis for this. 
# There’s no direct function for skewness or kurtosis in R or Python,
# but as you’ll see below, we can quickly calculate it 
# using the functions we already know.


## Skewness ########################

# Skewness describes whether the bulk of the distribution 
# sits to the left or right of the center.
# When people say that a certain person’s perspective is skewed,
# they mean, it’s very far from the mean. 
# In this case, we want to know, how skewed 
# are the heights of seawalls overall compared to the mean?
  
diff = sw - sw.mean()
diff**3
n = len(sw) - 1
sigma = sw.std()
sum(diff**3) / n
sum(diff**3) / (n * sigma**3)

# We could even write ourselves a function for it

def skewness(x):
  from pandas import Series
  x = Series(x)
  diff = x - x.mean()
  n = len(x) - 1
  sigma = x.std()
  output = sum(diff**3) / (n * sigma**3)
  return output


# Try it!
skewness(x = sw)

# Get skewness from a pandas series
sw.skew() # their formula differs slightly.


## Kurtosis  ########################

# Kurtosis describes how tightly bound the distribution is
# around the mean. Is it extremely pointy,
# with a narrow distribution (high kurtosis), 
# or does it span wide (low kurtosis)? 


# Like skew, we calculate how far each value is from the mean,
# but we take those differences to the 4th power, 
# which hyper-accentuates any extreme deviations 
# and returns only positive values. Then, we calculate 
# the sample-size adjusted average of those differences.
# Finally, to measure it in a consistent unit comparable
# across distributions, we divide by the standard deviation 
# taken to the 4th power; the powers in the numerator and 
# denominator then more-or-less cancel each other out.


diff = sw - sw.mean()
diff**4
n = len(sw) - 1
sigma = sw.std()
sum(diff**4) / n
sum(diff**4) / (n * sigma**4)


# We could even write ourselves a function for it
def kurtosis(x):
  from pandas import Series
  x = Series(x)
  diff = x - x.mean()
  n = len(x) - 1
  sigma = x.std()
  output = sum(diff**4) / (n * sigma**4)
  return output

# Try it!
kurtosis(sw)

# Get kurtosis from a pandas series
sw.kurtosis() # their formula differs slightly
sw.kurt()


# We can measure kurtosis! A pretty normal bell curve
# has a kurtosis of about 3, so our data doesn’t demonstrate
# much kurtosis. Kurtosis ranges from 0 to infinity 
# (it is always positive), and the higher it goes, 
# the pointier the distribution!
  
# Cleanup ##################################
globals().clear()
