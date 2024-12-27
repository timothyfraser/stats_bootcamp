# Training: Visualization with plotnine (aka ggplot) in Python!
# Tim Fraser


# Getting Started #################################

# Upgrade pip (if relevant)
# !/opt/python/3.8.17/bin/python3.8 -m pip install --upgrade pip

# Install main python packages for this training
# !pip install pandas
# !pip install plotnine
# !pip install os
# !pip install sys


# Import packages
import pandas as pd # import pandas 
from plotnine import * # import all plotnine visualization functions

# Import gapminder dataset
gapminder = pd.read_csv('C/gapminder.csv')

# Let's view it. (see console below)
gapminder


# Nice, we can see things more concisely.




# Your First Histogram with ggplot() ####################

# For a nice, customizable histogram,
# you can use the ggplot2 package's grammar of graphics syntax.

# We start with a blank plot with ggplot(), then we add (+) another layer using a geom_ function.
( ggplot() )
# We made an empty graph!

# In this case, let's add geom_histogram() to overlay a histogram
(ggplot() +
  geom_histogram(data = gapminder, mapping = aes(x = 'lifeExp')) )

# Time range
gapminder.year.min()
gapminder.year.max()

# number of unique countries
len(pd.Series(gapminder.country.unique()))




# What happens when you add alpha, changing its values in the 3 visuals below?
(ggplot() +
  geom_histogram(data = gapminder, mapping = aes(x = 'lifeExp'), 
                 alpha = 0.2) ) 

(ggplot() +
  geom_histogram(data = gapminder, mapping = aes(x = 'lifeExp'), 
                 alpha = 0.5) )

(ggplot() +
  geom_histogram(data = gapminder, mapping = aes(x = 'lifeExp'), 
                 alpha = 1) )


# We can make it more visually appealing. How would we adjust color?
# If you want to make it a single color, where do you need to write color = ...?

( ggplot() +
  geom_histogram(data = gapminder, mapping = aes(x = 'lifeExp'), 
                 color = "steelblue") )



# Looks like putting the name 'steelblue' INSIDE the aes() makes steelblue the name of a category,
# but putting the name 'steelblue' OUTSIDE the aes() makes the color steelblue.

# Finishing the Visual ###############################################
(ggplot() +
  geom_histogram(
    data = gapminder, mapping = aes(x = 'lifeExp'),
    color = "white",  # change outline color
    fill = "steelblue",  # change polygon fill
    binwidth = 5 # split up bins into every 5 years of life expectancy
  ) +
  # Add labels to aesthetics with labs()
  labs(x = "Life Expectancy (years)",
       y = "Frequency (count)",
       title = "Distribution of Life Expectancy",
       subtitle = "in 142 countries, 1952 - 2007",
       caption = "Source: gapminder dataset.") )


# Density Curves (function of the histogram) #################

# Alternatively, we could use geom_density() to
# map the approximate shape of that histogram as a line / function
(ggplot() +
  geom_density(data = gapminder, mapping = aes(x = 'lifeExp')) )


# A polished visual might look like this, customizing the color, fill, and labels
(ggplot() +
  geom_density(
    data = gapminder, mapping = aes(x = 'lifeExp'),
    color = "white",  # change outline color
    fill = "steelblue"  # change polygon fill
  ) +
  # Add labels to aesthetics with labs()
  labs(x = "Life Expectancy (years)",
       y = "Probability (density)",
       title = "Distribution of Life Expectancy",
       subtitle = "in 142 countries, 1952 - 2007",
       caption = "Source: gapminder dataset.") )


# Boxplots (summary statistics of distribution) ##################

# Alternatively, we could use boxplots to summarize this data by continent, describing:
# - median
# - interquartile range (25th to 75th percentiles)
# - outliers

(ggplot() +
  geom_boxplot(data = gapminder, mapping = aes(x = 'continent', y = 'lifeExp')) )


# A polished visual might look like this, customizing the color, fill, and labels
(ggplot() +
  geom_boxplot(
    data = gapminder, mapping = aes(x = 'continent', y = 'lifeExp'),
    color = "steelblue",  # change outline color
    fill = "white"  # change polygon fill
  ) +
  # Add labels to aesthetics with labs()
  labs(x = "Life Expectancy (years)",
       y = "Probability (density)",
       title = "Distribution of Life Expectancy",
       subtitle = "in 142 countries, 1952 - 2007",
       caption = "Source: gapminder dataset.") )



# Cleanup ################################

# Clear environment
globals().clear()
