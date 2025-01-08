# I1_code.R
# Cross-tabulation and Chi-squared
# Tim Fraser


# In this tutorial, we'll learn how evaluate 
# whether two categorical variables are statistically significantly related.
# We'll do this using the Chi-squared statistic,
# which evaluated whether the frequencies in a crosstable 
# are more extreme than expected at random.

# Import necessary libraries
# !pip install pandas
# !pip install pingouin

# Load packages
import pandas as pd
import pingouin as pg

# Import palmer penguins dataset, 
# recording traits of 344 penguins seen in Antarctica
penguins = pd.read_csv("I/palmerpenguins.csv")


# Researchers documented 344 penguins across multiple islands.
data = penguins[ ['species', 'island']]

# Let's count up group membership using pandas

# Penguins seen span 3 species
data.groupby('species').apply(lambda df: pd.Series({'n': len(df.species.dropna()) }))
# Penguins seen span 3 islands
data.groupby('island').apply(lambda df: pd.Series({'n': len(df.island.dropna()) }))

# Do certain species live disproportionately on a specific island?
data.groupby(['species', 'island'] ).apply(lambda df: pd.Series({ 'n': len(df.dropna()) }))

# Looks like the Gentoo penguins are much higher in number on Biscoe than on others.

# Is that difference statistically significant?

# Let's run the test using pingouin package's chi2_independence() function!
# See Documenation: https://pingouin-stats.org/build/html/generated/pingouin.chi2_independence.html
stat = pg.chi2_independence(data = data, x = 'species', y = 'island')


# View results!
stat[1] # see the cross-tabulation

# Looks like they calculated a BUNCH of different chi-squared statistics via different methods
# Pearson is the standard one to use.
stat[2].query('test == "pearson"')


# Here's the chi-squared statistic
stat[2].query('test == "pearson"')['chi2']


# pretty big - spans from 0 to infinity
# anything bigger than ~4 is pretty extreme

# And here's the p-value!
stat[2].query('test == "pearson"')['pval']


# Looks like this chi-squared statistic 
# is more extreme than 99.9% of chi-squared statistics 
# that you would get if this association 
# were just due to chance.

# Cleanup!
globals().clear()
