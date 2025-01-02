# Training: Visualization with ggplot in R!
# Tim Fraser


# Getting Started #################################

# install.packages("ggplot2")
# install.packages("readr")
library(ggplot2)
library(readr)


# Let's view it. (see console below)
gapminder = read_csv("C/gapminder.csv")

gapminder

# Nice, we can see things more concisely.

# Your First Histogram #################################

# For a really speedy glimpse at a distribution,
# you can use the built-in hist() function to get a simple histogram.

# Here's the distribution of life expectancies in countries over time from 1952 to 2007
hist(gapminder$lifeExp)

# time range
min(gapminder$year); max(gapminder$year)
# number of unique countries
length(unique(gapminder$country))



# Your First Histogram with ggplot() ####################

# For a nice, customizable histogram,
# you can use the ggplot2 package's grammar of graphics syntax.

# We start with a blank plot with ggplot(), then we add (+) another layer using a geom_ function.
ggplot()

# We made an empty graph!

# In this case, let's add geom_histogram() to overlay a histogram
ggplot() +
  geom_histogram(data = gapminder, mapping = aes( x = lifeExp ))



# What happens when you add alpha, changing its values in the 3 visuals below?
ggplot() +
  geom_histogram(data = gapminder, mapping = aes(x = lifeExp), 
                 alpha = 0.2)

ggplot() +
  geom_histogram(data = gapminder, mapping = aes(x = lifeExp), 
                 alpha = 0.5)

ggplot() +
  geom_histogram(data = gapminder, mapping = aes(x = lifeExp), 
                 alpha = 1)




# We can make it more visually appealing. How would we adjust color?
# If you want to make it a single color, where do you need to write color = ...?
# If you want to make it multiple colors according to a vector, where do you need to write color =?

# Run the following code:

# Version 1
ggplot() +
  geom_histogram(data = gapminder, mapping = aes(x = lifeExp), 
                 color = "steelblue")

# Version 2
ggplot() +
  geom_histogram(data = gapminder, mapping = aes(x = lifeExp, color = 'steelblue'))


# Looks like putting the name 'steelblue' INSIDE the aes() makes steelblue the name of a category,
# but putting the name 'steelblue' OUTSIDE the aes() makes the color steelblue.

# check it out!
colors()

# Finishing the Visual ###############################################

ggplot() +
  geom_histogram(
    data = gapminder, mapping = aes(x = lifeExp),
    color = "white",  # change outline color
    fill = "steelblue",  # change polygon fill
    binwidth = 5 # split up bins into every 5 years of life expectancy
  ) +
  # Add labels to aesthetics with labs()
  labs(x = "Life Expectancy (years)",
       y = "Frequency (count)",
       title = "Distribution of Life Expectancy",
       subtitle = "in 142 countries, 1952 - 2007",
       caption = "Source: gapminder dataset.")




# Density Curves (function of the histogram) #################

# Alternatively, we could use geom_density() to
# map the approximate shape of that histogram as a line / function
ggplot() +
  geom_density(data = gapminder, mapping = aes(x = lifeExp))


# A polished visual might look like this, customizing the color, fill, and labels
ggplot() +
  geom_density(
    data = gapminder, mapping = aes(x = lifeExp),
    color = "white",  # change outline color
    fill = "steelblue"  # change polygon fill
  ) +
  # Add labels to aesthetics with labs()
  labs(x = "Life Expectancy (years)",
       y = "Probability (density)",
       title = "Distribution of Life Expectancy",
       subtitle = "in 142 countries, 1952 - 2007",
       caption = "Source: gapminder dataset.")




# Boxplots (summary statistics of distribution) ##################

# Alternatively, we could use boxplots to summarize this data across groups, describing:
# - median
# - interquartile range (25th to 75th percentiles)
# - outliers

ggplot() +
  geom_boxplot(data = gapminder, mapping = aes(x = lifeExp, y = continent))




# A polished visual might look like this, customizing the color, fill, and labels
ggplot() +
  geom_boxplot(
    data = gapminder, mapping = aes(x = lifeExp, y = continent),
    color = "steelblue",  # change outline color
    fill = "white"  # change polygon fill
  ) +
  # Add labels to aesthetics with labs()
  labs(x = "Life Expectancy (years)",
       y = "Continent (n = 5)",
       title = "Distribution of Life Expectancy",
       subtitle = "in 142 countries, 1952 - 2007",
       caption = "Source: gapminder dataset.")



# Cleanup ################################

rm(list = ls())


