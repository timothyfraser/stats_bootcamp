# Workshop: Statistical Coding in Python
# Prof: Timothy Fraser

# New to Python? Run this script first! You'll gain comfort and familiarity.

# Welcome to Python in Posit Cloud! You made it!



# 1. Getting Started #######################################

# This document is an 'Python script.' (its name ends in .py).
# It contains two kinds of text:
# 1. 'code' - instructions to our statistical calculator
# 2. 'comments' - any text that immediately follows a '#' sign.
# Comments are ignored by the calculator, so we can write ourselves notes.


# Notice: 4 windows in RStudio.
# Window 1 (upper left): Scripts!
# Window 2 (bottom left): Console (this shows the output for our calculator)
# Window 3 (upper right): Environment (this shows any data the computer is holding onto for us)
# Window 4 (bottom right): Files (this shows our working project folder, our scripts, and any data files.)

# To change the background theme (and save your eyes),
# Go to Tools >> Global Options >> Appearance >> Editor Theme >> Dracula

# To increase the font size, 
# go to Tools >> Global Options >> Appearance >> Editor Font Size

# To make a script, go to File >> New File >> Python Script,
# then save it and name it.

# Let's learn to use Python!

# Upgrade pip
# Setup a virtual environment and install pip, the package manager
# Note: use THIS CODE, not the one in the video.
!python3 -m venv venv
!venv/bin/python -m pip install --upgrade pip

# Install main python packages for this course
# !pip install pandas
# !pip install scipy
# !pip install statsmodels
# !pip install patsy
# !pip install plotnine

# Print hello world!
print("hello world")

# Import libraries
import pandas as pd # Import pandas 


# Addition
1+2

# Vector
[1,2,3,4,5]

# Subtraction
5 - 2

# Multiplication
2 * 3

# Division
15 / 5

# Exponents
2**2

# Square Root
16**0.5

# Order of Operations
2 * 2 - 5

# Use parentheses!
2 * (2 - 5)


# Eg.
64**.5
64**(1/3)
8**2

# Types of Data in R


2 # this is a value
"x" # this is a vlue

myvalue = 2

secondvalue = myvalue + 2

# In RStudio, you can just print the values to console, 
# without using the print() command.
secondvalue


# Vectors
[1,2,3]
["Boston", "New York", "Los Angeles"]


# Here's a vector of (hypothetical) seawall heights in 10 towns.
myheights = [4, 4.5, 5, 5, 5, 5.5, 5.5, 6, 6.5, 6.5]

# And here's a list of hypothetical names for those towns
mytowns = ["Gloucester", "Newburyport", "Provincetown", 
             "Plymouth", "Marblehead", "Chatham", "Salem", 
             "Ipswich", "Falmouth", "Boston"]

# And here's a list of years when those seawalls were each built.
myyears = [1990, 1980, 1970, 1930, 1975, 1975, 1980, 1920, 1995, 2000]

# To manipulate them, we'll need to bundle them into pandas objects.


# let's bundle them into a data.frame with pandas.
sw = pd.DataFrame({'height': myheights, 'town': mytowns, 'year':myyears})
# Add 2 to all the heights
sw.height + 2

# Or just make it a series, and then add 2.
pd.Series(myheights) + 2


# Element-wise multiplication
pd.Series(myheights) * pd.Series(myheights)
 # or
sw.height * sw.height

# Matrix Multiplication...
sw.height.dot(sw.height)


# Descriptive Stats
sw.height.mean()
sw.height.median()
sw.height.min()
sw.height.max()
sw.height.mode()
sw.height.quantile(q = 0.5)



# Clear environment
globals().clear()
