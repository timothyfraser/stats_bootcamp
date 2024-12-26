#' @name D1_code.R
#' @author Prof. Tim Fraser
#' @description
#' Topic: Data Wrangling
#' 
#' Sometimes we need to edit and arrange our data better.
#' We call this 'data wrangling,' and it's a super useful skill.
#' Small functions can save you dozens of hours of work,
#' and it makes you really employable. 


# Plus, it's like tiny puzzles! Yay puzzles!

# Below, we're going to learn to use the dplyr package (pronounced 'dip-ler')
# There are several Tasks and Learning Checks (LC 1, LC2, etc.) in this tutorial, 
# Please run through them all to try it out yourself!

# 1. Load packages and Data (~1 min)

# 2. Using Pipelines (~1 min)

# 3. select() and rename() (~2 min)

# 4. mutate() (~4 min)

# 5. filter() and arrange() (~3 min)

# Please progress through each of these tasks 
# and answer the learning check questions as you go.
# In each task, you will 'discover' the uses of each function, 
# and make inferences together. 


# 0. SETUP ###################################

## 0.1 Load Packages and Data #################################

# First, install these packages with install.packages(),
# then load them with library(). 
# You need to use library() each session, but install.packages() only once.

install.packages(c("dplyr", "readr"))

library(dplyr) # for data wrangling
library(readr) # for reading in data

# We're going to use the nycflights datasets saved in our data/ folder.
# It's a compilation of several different tables.
# These tables describe all flights going out of New York City in 2013.
# It's a great big database of a massive socio-technical system.

airlines = read_csv("D/airlines.csv")
planes = read_csv("D/planes.csv")
flights = read_csv("D/flights.csv")
weather = read_csv("D/weather.csv")
airports = read_csv("D/airports.csv")
# Note: D/flights.csv is a really big table.
# Let's use D/flights_sample.csv, a random sample of 20000 flights
flights = read_csv("D/flights_sample.csv") 

# Let's view the flights dataset a few different ways

# View whole data.frame (gets censored)
flights
# View first 6 rows
head(flights)
# tilt it on its side and view all the columns
glimpse(flights)
# Or View() in its own window
View(flights)



## LC 1 #################################################

# Learning Check:
# What does a row refer to in the 'flights' dataset? 
# What does a row mean in the 'weather' dataset?



## 0.2 Using Pipelines ####################################

# The dyply package contains many useful functions, like glimpse().
# Another key function is the pipeline, represented by this symbol: %>%

# Pipelines connect data (dataframes, vectors, or values) to functions.


head(flights)
flights %>% head()


## LC 2 ######################################################

# Learning Check:
# Run the following functions. 
# Is the output for the following the same or different? What does the pipeline do?
# Why are pipelines helpful?

mean(weather$precip)
weather$precip %>% mean()



unique(weather$month) # ooh, a new function - what does unique() do?
weather$month %>% unique()

# ooh, another new function - what does length() do?

length(unique(weather$month))

# Take the month
weather$month %>%
  # get the unique values
  unique() %>%
  # get the length of the vector
  length()


# From now on, please always use pipelines when you can! 
# Life gets so much easier.



# 1. select() and rename() ###################################

# The dplyr package gives us several helpful functions 
# which we can pair with pipelines to make life easier.



## LC 3 ############################################

# Learning Check:
# Compare the following four chunks of code. 
# What does the select() function do? 
# Why do the contents of the select function matter?

# Chunk 1
flights

# Chunk 3
flights %>%
  select(dep_time, sched_dep_time)

# Chunk 3
flights %>%
  select(-year)

# Chunk 4
flights %>%
  select(contains("e"))




## LC 4 #############################################

# Learning Check:
# Compare the following chunks of code. 
# What does the rename() function do? How is it different from select?

flights

flights %>%
  select(departure_time = dep_time)

flights %>%
  select(month, day, departure_time = 4)

flights %>%
  rename(departure_time = dep_time)

flights %>%
  rename(departure_time = 4)



# 2. mutate() ###########################################

# Sometimes, we need to change values in a column (vector).
# We can do that by replacing an old vector with a new vector, 
# or just adding a new vector. mutate() helps us do that.

## LC 5 ###################################

# Learning Check:
# Compare the following chunks of code.

# What does the mutate function do? 
# Under what conditions can you use it?
# Why does it help us more than making calculations in the format of 'mydataframe$myvector - 1' ?

flights %>%
  mutate(dep_delay = dep_delay - 1)

flights$dep_delay - 1

flights %>%
  mutate(dep_delay = 1)

flights %>%
  mutate(dep_delay = dep_time - sched_dep_time)

flights %>%
  mutate(dep_delay = dep_time - sched_dep_time,
         arr_time = 0)

## LC 6 #########################################

# Learning Check:
# The values you assign a variable in mutate 
# must always be either just 1 value in length, 
# or the length of the data.frame (many rows in this case).

# Why? Because you can't fit 1000 values into 999 rows, for example.
# and because R knows to repeat 1 value 1000 times if you give it just 1 value, 
# but R won't know what to do otherwise.

# Check out the error we get below. Why does this happen?
airlines %>%
  mutate(value = 1)

airlines %>%
  mutate(funds = c(1, 2, 3))

# Do we get an error when we do the following two code chunks? Why or why not
airlines %>%
  mutate(funds = 1)

airlines %>%
  mutate(funds = rep(c(1,2,3,4),  4))

rep(c(1,2,3,4), 4)

airlines %>%
  mutate(funds = seq(from = 0, to = 4, length.out = 16))

airlines %>%
  mutate(funds = seq(from = 0, to = 4, length.out = n() )) ## ooh n(), a new dplyr function


# 3. filter() and arrange() #################################

## LC 7 #########################################################

# The filter() function is a real powerhouse for data wrangling.
# Compare the original purchases dataframe to when we apply the filter function. 
# What does it do in each situation? Please describe what it does above each chunk.

flights %>%
  filter(dep_delay > 0)

flights %>%
  filter(dep_delay == 0)

flights %>%
  filter(dep_delay != 0)

flights %>%
  filter(dep_delay %in% c(1,2))

flights %>%
  filter(!dep_delay %in% c(1,2))



## LC 8 #############################################

# Learning Check:
# Let's try some more complex ones. 
# What happens when you combine them? What's the difference between a comma, '&', and '|'?

flights %>%
  select(dep_delay, origin) %>%
  filter(dep_delay > 4, origin == "JFK") # JFK = JFK airport

flights %>%
  select(dep_delay, origin) %>%
  filter(dep_delay > 4 & origin == "JFK")

flights %>%
  select(dep_delay, origin) %>%
  filter(dep_delay > 4 | origin == "JFK")


## LC 9 ################################################

# Learning Check
# arrange() is a very powerful function. Compare the following code chunks. 
# What happens when you arrange by price? How does it change when we add desc(), or filter()?

flights %>%
  select(month, day, dep_delay, origin) %>%
  arrange(dep_delay)

flights %>%
  select(month, day, dep_delay, origin) %>%
  arrange(desc(dep_delay))

flights %>%
  select(month, day, dep_delay, origin) %>%
  arrange(origin, desc(dep_delay))

flights %>%
  select(month, day, dep_delay, origin) %>%
  filter(origin %in% c("JFK", "LGA")) %>%
  arrange(origin, desc(dep_delay))




# You're done!
# Let's clear your environment and empty the cache
rm(list = ls()); gc()