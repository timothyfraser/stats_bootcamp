# O2_code.py
# Demonstration of slides' code
# Tim Fraser

# The Ithaca Farmers Market is a vendor-owned cooperative that runs a
# Saturday-and-Sunday morning market for produce and hand made goods 
# on the Cayuga Lake waterfront.

# This Saturday, a volunteer tracked 500 customers 
# and recorded how many stalls each customer visited.

# The average customer visited a mean of 5.5 stalls
# and a median of 5 stalls, with a standard deviation of 2.5 stalls.

# But their spreadsheet got blown away into the lake! 
# Can we still estimate visitation patterns with these statistics?

# Getting Started #############################################

## Load Packages  ######################################

import pandas as pd;
import os; import sys
# Add distributions file
sys.path.append(os.path.abspath('O'))
from distributions import *

## Our data ############################################

# Let's approximate that data using a poisson distribution!

# Randomly sample 500 visits from a poisson distribution with a mean of 5.5
visits = rpois(n = 500, mu = 5.5)

# View it!
hist(visits)


# Finding probability densities ###########################

# Get the frequency for 5 visits in the distribution
dpois(5, mu = 5.5)

# Finding cumulative probabilities #######################

# What percentage of customers stopped by over 5 stalls?

# Get the cumulative frequency for a vlue (5) in the distribution
1 - ppois(5, mu = 5.5)

# Finding quantiles ########################################

# How many visits did people *usually* make? 
# Estimate the interquartile range (25th to 75th percentiles)
# of the unobserved distribution
qpois([0.25, 0.75], mu = 5.5)


# Cleanup! ##################################
globals().clear()

