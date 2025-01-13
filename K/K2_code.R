# K2_code.R
# Exercises

# Load packages
library(dplyr)
library(readr)
library(broom)
library(texreg)
library(gtools)


# Our data about disaster outcomes in Japanese municipalities over time
cities = read_csv("workshops/jp_matching_experiment.csv") %>% 
  # Tell R to treat year and pref as **ordered categories**
  mutate(year = factor(year),
         pref = factor(pref),
         by_tsunami = factor(by_tsunami, levels = c("Not Hit", "Hit")))

cities %>% glimpse()



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



# 2. Model the effect of each year on income. 
# Which year is not represented? The intercept represents that baseline category.
cities$year %>% unique()
m = cities %>% lm(formula = income_per_capita ~ year)
m 
# Calculate the predicted income per capita from 2011 to 2017.



# 3. Estimate the effect of being hit by the tsunami on income per capita, 
# controlling for damage rates.
m = cities %>% lm(formula = income_per_capita ~  damage_rate + by_tsunami)
tidier(m)

# Report the effect of being hit by the tsunami.
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# This effect has a 95% confidence interval from [A] to [B].
# This effect is statistically [significant? insignificant?] with a p-value of [XXX].




# 4. Model the effect of time on income per capita, 
# controlling for relevant traits.
m1 = cities %>% lm(formula = income_per_capita ~ pop_density + unemployment + 
                     damage_rate + by_tsunami + factor(year) )
m2 = cities %>% lm(formula = income_per_capita ~ pop_density + unemployment + 
                     damage_rate + by_tsunami + as.numeric(year) )

# View the resulting statistical table. 
# How does the information change when we control for year vs. each year? 
texreg::screenreg(l = list(m1, m2))



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




# Cleanup!
rm(list = ls())

