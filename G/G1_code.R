# G1_code.R
# Difference of Means (t-tests)
# Prof. Tim Fraser

# Load Packages
library(dplyr)
library(readr)
library(broom)

# Load data!
flights = read_csv("G/flights_sample.csv")

# JFK attempted to reduce departure delays in the month of April.
# Based on this sample of 20,000 flights, was there a 
# statistically significant difference in average departure delays in April compared to in March?
flights

# Get just flights in March and April
data = flights %>% 
  filter(month == 3 | month == 4) %>%
  select(month,dep_delay) 



# Compare the differences with descriptive statistics
data %>%
  group_by(month) %>%
  summarize(
    # get mean
    mean = mean(dep_delay, na.rm = TRUE),
    # calculate a standard error from std. deviation and sample size
    sd = sd(dep_delay, na.rm = TRUE),
    n = length(dep_delay[ !is.na(dep_delay)] ),
    se = sd / sqrt(n)
  )


# Looks like the month 4 had a higher average departure delay than month 3.
# Is this difference actually statistically significant? 
# Need t-test!



# Compare group variances. Are the variances significantly different?
var.test(dep_delay ~ month, data = data)

# Reject null hypothesis. These variances are fairly different.


# Run t-test, without equal variance assumption
m = t.test(dep_delay ~ month, data = data, var.equal = FALSE)

# Look at output
m

# Get statistics from model into a data.frame
stat = tidy(m)

# Get difference of means
stat$estimate

# Get t-statistic
stat$statistic

# Get p.value for t-statistic
stat$p.value

# Get confidence interval arounf difference of means
stat$conf.low
stat$conf.high


# Cleanup 
rm(list = ls())


