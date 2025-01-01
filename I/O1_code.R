# I1_code.R
# Cross-tabulation and Chi-squared
# Tim Fraser


# In this tutorial, we'll learn how evaluate 
# whether two categorical variables are statistically significantly related.
# We'll do this using the Chi-squared statistic,
# which evaluated whether the frequencies in a crosstable 
# are more extreme than expected at random.

# Load packages
library(dplyr)
library(readr)
library(broom)

# Import palmer penguins dataset, 
# recording traits of 344 penguins seen in Antarctica
data = read_csv("O/palmerpenguins.csv")


# Researchers documented 344 penguins across multiple islands.
# Penguins seen span 3 species
data %>% group_by(species) %>% count()
# Penguins seen span 3 islands
data %>% group_by(island) %>% count()

# Do certain species live disproportionately on a specific island?
data %>% group_by(species, island) %>% count()

# Looks like the Gentoo penguins are much higher in number on Biscoe than on others.

# Is that difference statistically significant?

# Let's run the test.
m = chisq.test(x = data$species, y = data$island)

# Extract a table of results with the broom package's tidy() function
stat = broom::tidy(m)

# Extract the chi-squared statistic
stat$statistic
# pretty big - spans from 0 to infinity
# anything bigger than ~4 is pretty extreme
# Extract p-value
stat$p.value

# Looks like this chi-squared statistic 
# is more extreme than 99.9% of chi-squared statistics 
# that you would get if this association 
# were just due to chance.

# Cleanup!
rm(list = ls())
