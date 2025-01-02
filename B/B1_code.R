# Training: Descriptive Statistics
# Tim Fraser


# This tutorial will introduce you to how to code
# and analyze distributions in R using descriptive statistics.

  
# Getting Started ##########################

# Please open up this script in your preferred computing environment;
# I recommend a Posit.Cloud project or (for Python only) Google Colabs.


# Our Data ####################

# We'll be looking at a vector of seawalls from 10 cities,
# measuring the height of each seawall.

# You could code it as a vector, 
# save it as an object, then use your functions!
sw = c(4.5, 5, 5.5, 5, 5.5, 6.5, 6.5, 6, 5, 4)

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
length(sw)

# Location #######################

# Where is our sample clustered? 
# What is the central tendency / most central values
# of the distribution?


## Mean #######################
mean(sw)

## Median ########################
median(sw)

## Mode ########################
mode(sw) # just kidding! R doesn't have a mode() function.

# But you could use this custom function I wrote instead; with some exceptions, it'll work in most cases.
mode = function(x){ as.numeric(names(sort(table(x), decreasing = TRUE))[1]) }
mode(sw)


# Spread (1) ###########################

# Spread: How much does our sample vary?


# What are the most extreme values?
# Percentiles
quantile(sw, probs = 0) # min
quantile(sw, probs = 1) # max

min(sw)
max(sw)

# Where do the middle-most 50% of values lie?
quantile(sw, probs = .25) # 25th percentile
quantile(sw, probs = .75) # 75th percentile




# Spread (2) ##########################

## Standard Deviation #####################

# But we can also evaluate how much our values vary 
# from the mean on average -
# the standard deviation, often abbreviated as  
# σ (sigma)

x = (sw - mean(sw))^2 # get squared deviations from mean
x = sum(x) # get sum
x = x / (length(sw) - 1) # divide by length - 1
x = x^0.5 # square root

x # view it

# Or, much more quickly...
sd(sw)

# Remove x
remove(x)



## Variance ########################

# Sometimes, we might want the variance,
# which is the standard deviation squared.
# This accentuates large deviations in a sample.

var(sw)

sd(sw)^2 # same!


## Coefficient of Variation (CV) ###############

# We could also calculate the coefficient of variation (CV),
# meaning how great a share of the mean
# does that average variation constitute?
# (Also put, how many times does the mean fit 
# into the standard deviation.)



# How many times does the mean fit into the standard deviation?
# How great a share of the mean does that average variation constitute?
sd(sw) / mean(sw)

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
var(sw) / length(sw)


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
se = sd(sw) / (length(sw)^0.5)
se = sd(sw) / sqrt(length(sw))
se 
# Or as:
(sd(sw)^2 / length(sw) )^0.5
# Or as
(var(sw) / length(sw))^0.5




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
  
# Get the differences from the mean
diff = sw - mean(sw)
diff^3
# Get the sample-size
# To be conservative, we'll subtract 1; this happens often in stats
n = length(sw) - 1
sigma = sd(sw)
# Now, we can calculate, on average, how big are these cubed differences?
sum(diff^3) / n
# How big are those cubed differences in terms of standard deviations,
# so we can compare with other samples?
sum(diff^3) / (n * sigma^3)

# We could even write ourselves a function for it
skewness = function(x){
  n = length(x) - 1
  diff = x - mean(x)
  sigma = sd(sw)
  output = sum(diff^3) / (n * sigma^3)
  return(output)
}


# Try it!
skewness(x = sw)


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

# Get ingredients...
diff = sw - mean(sw)
diff^4
n = length(sw) - 1
sigma = sd(sw)
# How big are the 4th-power deviations, on average?
sum(diff**4) / n
# How big on average in terms of standard deviations?
sum(diff**4) / (n * sigma**4)


# We could even write ourselves a function for it
kurtosis = function(x){
  n = length(x) - 1
  diff = x - mean(x)
  sigma = sd(sw)
  output = sum(diff^4) / (n * sigma^4)
  return(output)
}

# Try it!
kurtosis(sw)


# We can measure kurtosis! A pretty normal bell curve
# has a kurtosis of about 3, so our data doesn’t demonstrate
# much kurtosis. Kurtosis ranges from 0 to infinity 
# (it is always positive), and the higher it goes, 
# the pointier the distribution!
  
# Cleanup ##################################
rm(list = ls())
