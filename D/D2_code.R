#' D2_code.R
#' Practice Code
#' Lab: Modeling Carbon Footprints in Japan
#' Prof. Tim Fraser

# Load packages
library(dplyr)
library(readr)
library(ggplot2)


# This lab investigates trends in carbon emissions 
# in Japanese municipalities, from 2005 to 2017. 
# Japan held the landmark Kyoto Protocol in 1997, 
# which started international commitments to reduce 
# greenhouse gas emissions. 
# How much have Japanese cities reduced their carbon footprint,
# and which ones have succeeded the most? 

# In this lab, we hypothesize that each passing year has led
# to a statistically significant reduction in cities’ carbon footprints. 
# Let’s test that hypothesis!
  
  
# LOAD DATA ################################################

# In this dataset, each row is a city-year!
# We’ll calculate the carbon footprint for each city, 
# in kilotons of emissions per 1000 residents, 
# and we’ll zoom into just municipalities with at least 1 resident.


# Import data
jp <- read_csv("Q/jp_emissions.csv") %>%
  # to get the carbon footprint of each city,
  mutate(footprint = emissions / pop * 1000) %>%
  # Zoom into just cities where anyone lives
  filter(pop >= 1) %>%
  # Grab just these variables
  select(muni, footprint, year, pop)


# View the data!
jp %>% glimpse()

# View first 3 rows of dataset
jp %>% head(3)


# In this dataset, our variables mean:
# - muni: Name of Municipality, preceded by the prefecture where it is located (eg. Hokkaido [Prefecture] Sapporo-shi [City]).
# - footprint: city’s carbon footprint, adjusted for population size. The average kilotons of carbon emissions 1000 residents produce in a year.
# - year: year of observation (numeric).
# - pop: number of residents in that municipality, as of most recent census.



# Task 1: Average Carbon Footprints

# First, please calculate the average carbon footprint for 
# Japanese cities in each year, using group_by(), 
# and save it as a data.frame called avg.

# Now visualize the average carbon footprints for
# Japanese cities over time, using a scatterplot of your data.frame avg.
# Plot the line of best fit! What trend do we observe, on average?

avg <- jp %>%
  group_by(year) %>%
  summarize(footprint = mean(footprint, na.rm = TRUE))

# View it!
avg

# Visualize it!
ggplot() +
  geom_point(data = avg, mapping = aes(x = year, y = footprint)) +
  geom_line(data = avg, mapping = aes(x = year, y = footprint))



# Cleanup
rm(list = ls())



