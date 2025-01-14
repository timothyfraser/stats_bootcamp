# K2_code.R
# Multivariate Regression
# Exercises

# Load packages
library(dplyr)
library(readr)
library(broom)
library(texreg) # for texreg
library(gtools) # for our tidier() function


# Our data about disaster outcomes in Japanese municipalities over time
cities = read_csv("K/jp_matching_experiment.csv") %>% 
  # Tell R to treat year and pref as **ordered categories**
  mutate(year = factor(year),
         pref = factor(pref),
         by_tsunami = factor(by_tsunami, levels = c("Not Hit", "Hit")) )

cities %>% glimpse()

head(cities)


# Let's write a little tidier function..
tidier = function(model, ci = 0.95, digits = 3){
  model %>% # for a model object
    # get data.frame of coefficients
    # ask for a confidence interval matching the 'ci' above! 
    broom::tidy(conf.int = TRUE, conf.level = ci) %>% 
    # And round and relabel them
    reframe(
      term = term,  
      # Round numbers to a certain number of 'digits'
      estimate = estimate %>% round(digits),
      se = statistic %>% round(digits),
      statistic = statistic %>% round(digits),
      p_value = p.value %>% round(digits),
      # Get stars to show statistical significance
      stars = p.value %>% gtools::stars.pval(),
      # Get better names
      upper = conf.high %>% round(digits),
      lower = conf.low %>% round(digits))
}



# 1. Compare these two data.frames. 
# What does it mean to estimate an intercept-only model?

# Intercept-only model
cities %>% lm(formula = income_per_capita ~ 1)
# Descriptive Stats
cities %>% summarize(mean = mean(income_per_capita))


# Answers:
# An intercept-only model predicts the outcome 
# by literally taking the mean of the outcome.


# 2. Model the effect of each year on income. 
# Which year is not represented? The intercept represents that baseline category.
cities$year %>% unique()
m = lm(formula = income_per_capita ~ year, data = cities)
m 
# Calculate the predicted income per capita from 2011 to 2017.


# Answers:
# 2011 is not represented; 2011 is the baseline category for comparison.
# 1.0564901 + -0.0335762 --> 1.022914 in 2012
# ...
# 1.0564901 + 0.1021192  --> 1.158609 in 2017



# 3. Estimate the effect of being hit by the tsunami on income per capita, 
# controlling for damage rates.
m = lm(formula = income_per_capita ~  damage_rate + by_tsunami, data = cities)
tidier(m)

# Report the effect of being hit by the tsunami.
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# This effect has a 95% confidence interval from [A] to [B].
# This effect is statistically [significant? insignificant?] with a p-value of [XXX].


# Answers:

# Report the effect of being hit by the tsunami.
# When hit by the tsunami (1 vs. 0), the income per capita in millions of yen per capita 
# increases by +0.032 millions of yen per capita.
# This effect has a 95% confidence interval from -0.001 to 0.066.
# This effect is statistically **insignificant?** at a 95% confidence level, with a p-value of 0.058.
# This effect is statistically significant at a 90% confidence level, because 0.058 < p = 0.10.





# 4. Model the effect of time on income per capita, 
# controlling for relevant traits.
m1 = cities %>% lm(formula = income_per_capita ~ pop_density + unemployment + 
                     damage_rate + by_tsunami + factor(year) )
m2 = cities %>% lm(formula = income_per_capita ~ pop_density + unemployment + 
                     damage_rate + by_tsunami + as.numeric(year) )

# View the resulting statistical table. 
# How does the information change when we control for year vs. each year? 
texreg::screenreg(l = list(m1, m2))


# See video for discussion.



# 5. Normalize these demographic covariates
# (mean = 0, in units of standard deviation from the mean)
# Now model them. 
cities %>%
  mutate(pop_density = scale(pop_density),
         unemployment = scale(unemployment),
         damage_rate = scale(damage_rate)) %>%
  lm(formula = income_per_capita ~ pop_density + unemployment + 
       damage_rate + by_tsunami + year)

# Report the population density vs. unemployment, damage_rate
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# Which effect size is largest?
# Which effect sizes can you NOT compare?




# Answers:

# As the population density increases by 1 standard deviation,
# the income per capita is expected to increase by 0.18 millions of yen per capita.

# As the unemployment rate increases by 1 standard deviation,
# the income per capita is expected to decrease by 0.05 millions of yen per capita.

# As the damage rate increases by 1 standard deviation,
# the income per capita is expected to decrease by 0.01 millions of yen per capita.

# You can compare pop_density, unemployment, and damage_rate,
# because they are all in units of standard deviations.

# You can't compare effects of numeric predictors against effects of categorical predictors,
# because they're fundamentally different - eg. standard deviations versus 0/1


# Cleanup!
rm(list = ls())

