#' @name D1_code.py
#' @author Prof. Tim Fraser
#' @description
#' Topic: Data Wrangling
#' 
#' Sometimes we need to edit and arrange our data better.
#' We call this 'data wrangling,' and it's a super useful skill.
#' Small functions can save you dozens of hours of work,
#' and it makes you really employable. 

# Plus, it's like tiny puzzles! Yay puzzles!

# Below, we're going to learn to use the pandas package
# There are several Tasks and Learning Checks (LC 1, LC2, etc.) in this tutorial, 
# Please run through them all to try it out yourself!

# Please progress through each of these tasks 
# and answer the learning check questions as you go.
# In each task, you will 'discover' the uses of each function, 
# and make inferences together. 


# 0. SETUP ###################################

## 0.1 Load Packages and Data #################################

# First, install these packages with pip,
# then load them with from / import. 
# You need to load them each session, but install only once

# uncomment this script and run it.
# !pip install pandas

# Load pandas as object pd
import pandas as pd



# We're going to use the nycflights datasets saved in our D/ folder.
# It's a compilation of several different tables.
# These tables describe all flights going out of New York City in 2013.
# It's a great big database of a massive socio-technical system.

airlines = pd.read_csv("D/airlines.csv")
planes = pd.read_csv("D/planes.csv")
flights = pd.read_csv("D/flights.csv")
weather = pd.read_csv("D/weather.csv")
airports = pd.read_csv("D/airports.csv")

del flights

# Note: D/flights.csv is a really big table.
# Let's use D/flights_sample.csv, a random sample of 20000 flights
flights = pd.read_csv("D/flights_sample.csv") 

# Let's view the flights dataset a few different ways

# View whole data.frame (gets censored)
flights

# View first 6 rows
flights.head()

# View more rows
flights.head(7)

# View specific rows 
flights.values[1:3,]

flights[0:4]


## LC 1 #################################################

# Learning Check:
# What does a row refer to in the 'flights' dataset? 
# What does a row mean in the 'weather' dataset?
flights

weather.columns

## 0.2 Using the dot ####################################

# A key tool is the '.' in python, which lets you perform certain functions
# on objects with specific classes. Pandas objects have a lot of built in functions that can work on them.

# Here's an example
flights.head()


flights.dep_time.mean()

## LC 2 ######################################################

# Learning Check:
# Run the following functions. 
# Is the output for the following the same or different? What does the dot do?
# Why is the dot helpful?

weather.precip.mean()

sum(weather.precip) / len(weather.precip)




# From now on, please always use the dot when you can! 
# Life gets so much easier.



# 1. naming and indexing columns ###################################

# pandas gives us several helpful functions which we can pair with the dot
# to make life easier.


## LC 3 ############################################

# Learning Check:
# Compare the following four chunks of code. 
# What does these pandas function do? 

# Chunk 1
flights

# Chunk 2
flights[ ['dep_time', 'sched_dep_time'] ]

# Chunk 3
flights.drop(columns = ['year'])

# Chunk 4 
flights.filter(like = 'e')




## LC 4 #############################################

# Learning Check:
# Compare the following chunks of code. 

# Chunk 1
flights

# Chunk 2
flights.columns

# Chunk 3
flights.rename(columns={'dep_time': 'departure_time'}).columns


# Chunk 4
flights.rename(columns={'dep_time': 'departure_time'})[[ 'departure_time' ]]

# Chunk 5
flights.iloc[:, 3]

# Chunk 6
f2 = flights[[ 'month', 'day']].copy()
f2
f2['departure_time'] = flights.iloc[:,3]
# OR
f2['departure_time'] = flights.dep_time

f2


# 2. appending  ###########################################


# Sometimes, we need to change values in a column (vector).
# We can do that by replacing an old vector with a new vector, 
# or just adding a new vector. 

## LC 5 ###################################

# Learning Check:
# Compare the following chunks of code.

# How do you overwrite vectors in a pandas dataframe?

flights['dep_delay'] = flights['dep_delay'] - 1
flights['dep_delay']

flights['dep_delay'] - 1




## LC 6 #########################################

# Learning Check:
# The values you assign a variable in MUTATE operations like append
# must always be either just 1 value in length, 
# or the length of the data.frame (many rows in this case).

# Why? Because you can't fit 1000 values into 999 rows, for example.
# and because Python knows to repeat 1 value 1000 times if you give it just 1 value, 
# but Python won't know what to do otherwise.

# Check out the error we get below. Why does this happen with the second, but not the first chunk?

# chunk 1
airlines['value'] = 1
airlines

# chunk 2
airlines['funds'] = [1,2,3]



# Do we get an error when we do the following two code chunks? Why or why not
# chunk 1
airlines['funds'] = 1
airlines

# chunk 2
airlines['funds'] = [ 1,2,3,4,  1,2,3,4,  1,2,3,4,  1,2,3,4  ]
airlines

# Some tricks for getting the right number of values
airlines['funds'] = range(1, 16+1)
airlines

airlines['funds'] = range(1, len(airlines)+1)
airlines


# 3. filter() and arrange() #################################

## LC 7 #########################################################

# The query() and isin() functions are real powerhouses for data wrangling.
# Compare the original flights dataframe to when we apply these functions. 
# What does it do in each situation? Please describe what it does above each chunk.

# chunk 1
flights.query('month > 0')

# chunk 2
flights.query('month == 4')

# chunk 3
flights.query('month != 4')

# chunk 4
flights[ flights['month'].isin([1,2]) ]

flights[  flights.month.isin( [1,2] )  ]


# chunk 5
flights[ ~flights['month'].isin( [1,2] ) ]



## LC 8 #############################################

# Learning Check:
# Let's try some more complex ones. 
# What happens when you combine them? What's the difference between an 'and' and an 'or'

# chunk 1
flights[ ['dep_delay', 'origin'] ].query('dep_delay > 4 and origin == "JFK"')
# note: JFK = JFK airport

# chunk 2
flights[ ['dep_delay', 'origin'] ].query('dep_delay > 4 or origin == "JFK"')




## LC 9 ################################################

# Learning Check
# sort_values() is a very powerful function. Compare the following code chunks. 
# What happens when you arrange by departure delays? How does it change when we add ascending = False?

flights[['month', 'day', 'dep_delay', 'origin']].sort_values(by='dep_delay')

flights[['month', 'day', 'dep_delay', 'origin']].sort_values(by='dep_delay', ascending=False)

flights[['month', 'day', 'dep_delay', 'origin']].sort_values(by=['origin', 'dep_delay'], ascending=[True, False])

flights[['month', 'day', 'dep_delay', 'origin']].loc[flights['origin'].isin(['JFK', 'LGA'])].sort_values(by=['origin', 'dep_delay'], ascending=[True, False])

flights[['month', 'day', 'dep_delay', 'origin'] ].loc[flights['origin'].isin(['JFK', 'LGA'])].sort_values(by=['origin', 'dep_delay'], ascending=[True, False])

flights[ flights.origin.isin(['JFK', 'LGA']) ][ [ 'month', 'day', 'dep_delay', 'origin' ] ].sort_values(by=['origin', 'dep_delay'], ascending=[True, False])


# As these get longer, it can help to break them up into multiple lines.

flights[ 
  flights.origin.isin(['JFK', 'LGA']) 
  ][ [ 'month', 'day', 'dep_delay', 'origin' ] 
  ].sort_values(
    by=['origin', 'dep_delay'], 
    ascending=[True, False]
    )

# Cleanup ###################################
# You're done!
# Let's clear your environment and empty the cache
globals().clear()
