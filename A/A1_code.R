# Workshop: Statistical Coding in R
# Prof: Timothy Fraser

# New to R? Run this script first! You'll gain comfort and familiarity.

# Welcome to RStudio in Posit Cloud! You made it!



# 1. Getting Started #######################################

# This document is an 'R script.' (its name ends in .R).
# It contains two kinds of text:
# 1. 'code' - instructions to our statistical calculator
# 2. 'comments' - any text that immediately follows a '#' sign.
# Comments are ignored by the calculator, so we can write ourselves notes.


# Notice: 4 windows in R.
# Window 1 (upper left): Scripts!
# Window 2 (bottom left): Console (this shows the output for our calculator)
# Window 3 (upper right): Environment (this shows any data the computer is holding onto for us)
# Window 4 (bottom right): Files (this shows our working project folder, our scripts, and any data files.)

# To change the background theme (and save your eyes),
# Go to Tools >> Global Options >> Appearance >> Editor Theme >> Dracula

# To increase the font size, 
# go to Tools >> Global Options >> Appearance >> Editor Font Size

# To make a script, go to File >> New File >> R Script,
# then save it and name it.

# Let's learn to use R!



# 2. Basic Calculations in R #######################################

# Try highlighting the following with your cursor, 
# and then press control and enter simultaneously,
# or the 'Run' button above.

1 + 5 # Addition

5 - 2 # Subtraction

2 * 3 # Multiplication

15 / 5 # Division

2^2 # Exponents

sqrt(4) # Square-Roots




# 3. Types of Values in R  #######################################

# R accepts 2 type of data:

# Numeric Values
15000
0.0005
-8222 # notice no commas allowed

# Character Strings
"Coding!" # Uses quotation marks
"Corgis!" # Can contain anything - numbers, characters, etc.
"Coffee!"

# And something called Factors, 
# which are characters, but have a specific order
# We'll learn them later.



# 4. Types of Data in R  #######################################

##### First,
# R uses **values** - which are single numbers or characters.

2 # this is a value
"x" # this is also a value

# You can save a value as a named 'object' in the R Environment.
# That means, we tell R to remember that 
# whenever you use a certain name, it means that value.

# To name something as an object, use an arrow!
myvalue <- 2
myvalue = 2

# Now let's highlight and press control enter on myvalue.
# Notice how it's listed in the R Environment (upper right)
# and how it outputs as 2 in the console?
myvalue

# We can do operations too
secondvalue = myvalue + 2 # add 2 to myvalue
secondvalue # check new value - oooh, it's 4!

# We can also overwrite old objects with new objects 
myvalue <- "I overwrote it!"
myvalue

# And we can also remove objects from the Environment
remove(myvalue, secondvalue)




##### Second, 
# R contains values in **vectors**, which are sets of values.

# This is a numeric vector
c(1, 4, 8) # is the same as 1, 4, 8

# This is a character vector
c("Boston", "New York", "Los Angeles")

# This doesn't work - R immediately makes it into a character vector
c(1, "Boston", 2)

# You can do mathematical operations 
# on entire vectors of values, all at once.
c(1,2,3,4) * 2 # this multiplies each value by 2!
c(1,2,3,4) + 2 # this adds 2 to each value!


# We can save vectors as objects too!

# Here's a vector of (hypothetical) seawall heights in 10 towns.
myheights = c(4, 4.5, 5, 5, 5, 5.5, 5.5, 6, 6.5, 6.5)

# And here's a list of hypothetical names for those towns
mytowns = c("Gloucester", "Newburyport", "Provincetown", 
             "Plymouth", "Marblehead", "Chatham", "Salem", 
             "Ipswich", "Falmouth", "Boston")

# And here's a list of years when those seawalls were each built.
myyears <- c(1990, 1980, 1970, 1930, 1975, 1975, 1980, 1920, 1995, 2000)

# We can still do operations on entire vectors!
myyears + 1


##### Third, 
# R bundles vectors into data.frames.

# Using the data.frame command, we make a data.frame,
data.frame(
  height = myheights, # length 10
  town = mytowns, # length 10
  year = myyears) # length 10




# And inside, we put a bunch of vectors of EQUAL LENGTHS
# Give each vector a name

# And when it outputs in the console, it looks like a spreadsheet!
# BECAUSE ALL SPREADSHEETS ARE **DATAFRAMES!**
# AND ALL COLUMNS ARE **VECTORS!**
# AND ALL CELLS ARE **VALUES!**

# Actually, we can make data.frames into objects too!

# Let's name our data.frame about seawalls 'sw'
sw = data.frame(
  height = myheights,
  town = mytowns,
  year = myyears) # Notice this last parenthesis; very important


sw


sw$height
sw$town

# Although, we could do this too, and it would be equivalent
sw <- data.frame(
  # It's okay to split code across multiple lines.
  # It keeps things readable.
  height = c(4, 4.5, 5, 5, 5, 
             5.5, 5.5, 6, 6.5, 6.5),
  town = c("Gloucester", "Newburyport", "Provincetown", 
           "Plymouth", "Marblehead", "Chatham", "Salem",
           "Ipswich", "Falmouth", "Boston"),
  year = c(1990, 1980, 1970, 1930, 1975, 
           1975, 1980, 1920, 1995, 2000)) 

sw


# Let's check out our dataframe!
sw

# But what if we want to work with the vectors again?
# We can use the '$' sign to say, 
# grab the following vector from inside this data.frame


sw$height


sw$height + 1

# we can also update values, like the following:
# sw$height <- sw$height + 1
# I've put this in comments, since I don't actually want to do it,
# but good to know, right?




# 5. Descriptive Statistics in R  #######################################

# We can run functions that come pre-installed to analyze vectors.
# These include: mean(), median(), sum(), min(), max(), range(), sd()

# Measures of Central Tendency
mean(sw$height) # the mean seawall height among these towns
median(sw$height) # the median seawall height
sum(sw$height) # total meters of seawall height! (weird number, but okay)

# Measures of Dispersion
min(sw$height) # smallest seawall height
max(sw$height) # tallest seawall height
range(sw$height) # range of seawalls (min & max)
sd(sw$height) # the standard deviation of seawall heights


# That's really fast!


# 6. Missing Data  #######################################

# Sometimes, data.frames include missing data for a case/observation
# For example, let's say there is an 11th town, where the seawall height is unknown.

# We would write:
mysw <- c(4, 4.5, 5, 5, 5,
          5.5, 5.5, 6, 6.5, 6.5, NA) # see the 'NA' for non-applicable
mysw

# If you run mean(mysw) now, R doesn't know how to add 6.5 + NA
# The output will become NA instead of 5.35
mean(mysw)

# To fix this, we can add an 'argument' to the function,
# telling it to omit NAs from the calculation
mean(mysw, na.rm = TRUE) # short for, 'remove NAs'
# Pretty cool, no?

# Each function is unique, often made by different people,
# so only these functions have na.rm as an argument.


# Throughout the rest of the course, 
# we're going to advance each of these skills:
# - working with types of data in R
# - calculating meaningful statistics in R
# - visualizing meaningful trends in R




# 7. Removing Data  #######################################

# Be sure to clear your environment often.
# That means, using remove() or the broom tool in the upper right hand corner.
remove(mysw)
# Easier to use rm(), which removes everything at once.
rm(list = ls())

# You can clean your console too, using broom in console's upper right corner.

# Save often. (Control + Save usually works on PC)

# You can download files using more / export, or upload them.




# 8. Reading and Writing data ###################################

# To read and write data to file, we need an extra package - readr!
# We can install and load the readr package to get access to its read_csv() and write_csv() functions.
# To install readr, we use install.packages() one time.
install.packages("readr")

# To load readr, we use library() (every session)
library(readr)

# Let's take that sw data.frame and write it to file.

# Although, we could do this too, and it would be equivalent
sw <- data.frame(
  # It's okay to split code across multiple lines.
  # It keeps things readable.
  height = c(4, 4.5, 5, 5, 5, 
             5.5, 5.5, 6, 6.5, 6.5),
  town = c("Gloucester", "Newburyport", "Provincetown", 
           "Plymouth", "Marblehead", "Chatham", "Salem",
           "Ipswich", "Falmouth", "Boston"),
  year = c(1990, 1980, 1970, 1930, 1975, 
           1975, 1980, 1920, 1995, 2000)) 


# write the objects sw to the file path A/sw.csv
write_csv(sw, file = "A/sw.csv")

# Let's remove the object sw
remove(sw)

# Now let's read it back in and assign it to an object!
sw = read_csv("A/sw.csv")

# View it!
sw

# remove it
remove(sw)

# You'll be a rockstar at using R in no time!
# Stay tuned for our next Workshop!




### Troubleshooting:

# If your session freezes, go to 'Session' >> 'Restart R.' 
# If that doesn't work, go to 'Session' >> 'Terminate'. 
# If that doesn't work, click on the elipsis (...) in the white banner at the top
# and select Relaunch Project.
# If that doesn't work, let me know! 

# Having problems? There are three causes of most all problems in R.
# 1. there's a missing parenthesis or missing quotation mark in one's code.
# 2. You're using a function from a package that needs to be loaded. 
# (we'll talk about this later.)
# 3. Too much data in your environment is causing R to crash. Clear the environment.
