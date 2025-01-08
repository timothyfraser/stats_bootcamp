# H1_code.py
# Analysis of Variance (ANOVA)
# Prof. Tim Fraser

# Import necessary libraries
# !pip install pandas
# !pip install scipy
# !pip install pingouin

import pandas as pd
from scipy.stats import bartlett
import pingouin as pg

# Load the dataset
flights = pd.read_csv("H/flights_sample.csv")

# JFK attempted to reduce departure delays in the year 2013.
# Looking at the 8 carriers with the largest volume of flights,
# were there statistically significant differences in departure delays by carrier in April?

# Filter data for the year 2013 and the 8 selected carriers
data = flights.query('year == 2013')
data = data[ data['carrier'].isin(["UA", "B6", "EV", "DL", "AA"]) ]
data = data[ ['carrier', 'dep_delay'] ]

# Extract the dep_delay vector for each of these 5 carriers
a = data.query('carrier == "UA"')['dep_delay']
b = data.query('carrier == "B6"')['dep_delay']
c = data.query('carrier == "EV"')['dep_delay']
d = data.query('carrier == "DL"')['dep_delay']
e = data.query('carrier == "AA"')['dep_delay']

# Perform Bartlett's test for homogeneity of variances

# Extract a set of dep_delays per carrier
# Calculate the F statistic and p-value for the test
b_stat, b_p_value = bartlett(a,b,c,d,e)
# Report the results
print(f"Bartlett's test statistic: {b_stat}, p-value: {b_p_value}")

# If p-value < 0.05, variances are significantly different
var_equal = b_p_value >= 0.05
# If variances are significantly different, do not assume equal variance in ANOVA
print(var_equal)


# Perform one-way ANOVA with unequal variances (Welch's ANOVA))
# See documentation: https://pingouin-stats.org/build/html/generated/pingouin.welch_anova.html#pingouin.welch_anova
stat = pg.welch_anova(dv='dep_delay', between='carrier', data=data)

# If equal variances, use standard ANOVA with pg.anova()
# See documentation: https://pingouin-stats.org/build/html/generated/pingouin.anova.html
# stat = pg.anova(dv = 'dep_delay', between = 'carrier', data = data)

# View the ANOVA table
print(stat)

# Extract F-statistic and p-value
stat['F']
stat['p-unc']

# Cleanup
globals().clear()
