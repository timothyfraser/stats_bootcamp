# N1_code.R
# Analysis of Variance (ANOVA)
# Prof. Tim Fraser

# Load Packages
library(dplyr)
library(readr)
library(broom)

# Load data!
flights = read_csv("M/flights_sample.csv")

# JFK attempted to reduce departure delays in the year 2013.
# Looking at the 5 carriers with largest volume of flights,
# were there statistically significant differences in departure delays by carrier in April?

# Get just flights in 2013
data = flights %>% 
  filter(year == 2013) %>%
  filter(carrier %in% c("UA", "B6", "EV", "DL", "AA")) %>%
  select(carrier, dep_delay)

# Looks like the month 4 had a higher average departure delay than month 3.
# Is this difference actually statistically significant? 
# Need t-test!


# Compare group variances. Are the variances significantly different?
# Are the variances of my 3+ groups significantly different?
# Homogeneity of Variance - Barlett's test for K^2
bartlett.test(dep_delay ~ carrier, data = data)

# K-squared is a ratio showing how different are the variances, from 0 to infinity.
# If K-squared is not significant, the differences are not significant.

# Looks like the differences in variance are quite significant.
# Best **not** to assume equal variance.

# You can do an ANOVA without the equal variance assumption using oneway.test()
# set var.equal = FALSE if no equal variance assumption.
m = oneway.test(dep_delay ~ carrier, data = data, var.equal = FALSE)

# if equal variance assumption, set var.equal = TRUE
# m = oneway.test(dep_delay ~ carrier, data = data, var.equal = TRUE)


# View table
m %>% tidy()

# Get F statistic
m$statistic
# Get significance
m$p.value



# Cleanup 
rm(list = ls())


