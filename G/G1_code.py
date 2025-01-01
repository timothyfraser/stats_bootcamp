# G1_code.py
# Difference of Means (t-tests)
# Prof. Tim Fraser

# Import necessary libraries
# !pip install pandas
# !pip install scipy
# !pip install pingouin

import pandas as pd
from scipy.stats import bartlett
import pingouin as pg

# Load the dataset
flights = pd.read_csv("M/flights_sample.csv")

# JFK attempted to reduce departure delays in the month of April.
# Based on this sample of 20,000 flights, was there a 
# statistically significant difference in average departure delays in April compared to in March?
flights

# Get just flights in March and April
data = flights.query('year == 2013')
data = data.query('month == 3 or month == 4')
data = data[ ['month', 'dep_delay'] ]
data


# Compare the differences with descriptive statistics
data.groupby('month').apply(lambda df: pd.Series({
  # get mean
  'mean': df.dep_delay.mean(),
  # calculate a standard error from std. deviation and sample size
  'sd': df.dep_delay.std(),
  'n': len(df.dep_delay.dropna()),
  'se': df.dep_delay.std() / len(df.dep_delay)**0.5
}))


# Looks like the month 4 had a higher average departure delay than month 3.
# Is this difference actually statistically significant? 
# Need t-test!



# Compare group variances. Are the variances significantly different?
# Extract the dep_delay vector for these 2 months
a = data.query('month == 3')['dep_delay']
b = data.query('month == 4')['dep_delay']

# Perform Bartlett's test for homogeneity of variances

# Extract a set of dep_delays per month
# Calculate the F statistic and p-value for the test
b_stat, b_p_value = bartlett(a,b)
# Report the results
print(f"Bartlett's test statistic: {b_stat}, p-value: {b_p_value}")

# If p-value < 0.05, variances are significantly different
var_equal = b_p_value >= 0.05
# If variances are significantly different, do not assume equal variance in t-test
print(var_equal)



# Perform unpaired t-test with equal variances (correction = False)
# See documentation: https://pingouin-stats.org/build/html/generated/pingouin.ttest.html
stat = pg.ttest(y = data['dep_delay'], x = data['month'], paired = False, correction = 'False')

# Perform unpaired t-test with uneqaul variances (correction = True --> Welch T-test)
# See documentation:  https://pingouin-stats.org/build/html/generated/pingouin.ttest.html
# stat = pg.ttest(y = data['dep_delay'], x = data['month'], paired = False, correction = 'True')

# View the t-test table
print(stat)

stat['T'] # extract t-statistic
stat['CI95%'] # extract 95% confidence interval
stat['p-val'] # extract p-value

# Compares group 1 with group 2 (whatever category comes first alphabetically)
# eg. avg of month 3 minus avg of month 4


# Cleanup
globals().clear()

