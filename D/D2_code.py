#' D2_code.py
#' Practice Code
#' Lab: Modeling Carbon Footprints in Japan
#' Prof. Tim Fraser

# Install packages
# !pip install pandas
# !pip install plotnine

# Load packages
import pandas as pd
from plotnine import *

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
jp = pd.read_csv("D/jp_emissions.csv")

# Data wrangling
data = jp[ ['muni', 'year', 'pop', 'emissions'] ]

# Zoom into just cities where anyone lives
data = data.query('pop >= 1')
# Get the carbon footprint of each city,
data['footprint'] = data['emissions'] / data['pop'] * 1000
# Grab just these variables
data = data[['muni', 'footprint', 'year', 'pop']]


# View the data!
data


# Describe the data!
data.describe()

# View first 3 rows of dataset
data.head(3)


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


# Get mean footprint per year, with options of getting extra stats
avg = data.groupby('year').apply(lambda df: pd.Series({
  'mean': df.footprint.dropna().mean()  })
  ).reset_index()



# View it!
avg


# Alternative methods:

# Get mean footprint per year
data.groupby('year')[ 'footprint' ].mean().reset_index()

# Get all descriptive stats for footprint per year
data.groupby('year')['footprint'].describe().reset_index()


# Visualize it!
(ggplot() +
  geom_point(data = avg, mapping = aes(x = 'year', y = 'mean')) +
  geom_line(data = avg, mapping = aes(x = 'year', y = 'mean')) )



# Cleanup
rm(list = ls())



