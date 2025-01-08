# G1_code.R
# Difference of Means (t-tests)
# Prof. Tim Fraser

# Load Packages
# install.packages(c("dplyr", "readr", "broom"))
library(dplyr) # for data wrangling
library(readr) # for reading data
library(broom) # for convert models to data.frames

# Load data!
flights = read_csv("G/flights_sample.csv")

# JFK attempted to reduce departure delays in the month of April.
# Based on this sample of 20,000 flights, was there a 
# statistically significant difference in average departure delays in April compared to in March?
flights

# Get just flights in March and April
data = flights %>% 
  filter(month == 3 | month == 4) %>%
  select(month,dep_delay) %>%
  # Filter to just valid data
  filter(!is.na(dep_delay))

data

# Compare the differences with descriptive statistics
data %>%
  group_by(month) %>%
  reframe(
    # get mean
    mean = mean(dep_delay, na.rm = TRUE),
    # calculate a standard error from std. deviation and sample size
    sd = sd(dep_delay, na.rm = TRUE),
    n = n(),
    # n = length(dep_delay[ !is.na(dep_delay)] )
    se = sd / sqrt(n)
  )


# Looks like the month 4 had a higher average departure delay than month 3.
# Is this difference actually statistically significant? 
# Need t-test!



# Compare group variances. Are the variances significantly different?
var.test(formula = dep_delay ~ month, data = data)


# Reject null hypothesis. These variances are fairly different.


# Run t-test, without equal variance assumption
m = t.test(formula = dep_delay ~ month, data = data, var.equal = FALSE)

# Look at output
m

# Get statistics from model into a data.frame
stat = broom::tidy(m)

stat

# Get difference of means
stat$estimate


# Get t-statistic
stat$statistic


# Get p.value for t-statistic
stat$p.value

# 16% of random t stats are more extreme than mine.
# My observed t stat is more extreme than 84% of random t-stats.

# Cutoffs

# Get 95% confidence interval around difference of means
stat$conf.low
stat$conf.high


# Cleanup 
rm(list = ls())


