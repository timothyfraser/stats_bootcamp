# Q3_code.R
# Workshop: Iteration with purrr in R
# Prof: Timothy Fraser

# Now that we know how to write functions and use loops, let's learn a more 
# elegant way to apply functions to multiple items: the purrr package!
# 
# The purrr package provides powerful tools for iteration (repeating operations).
# Instead of writing for loops, we can use map() functions to apply a function
# to each element in a list or vector. This is often cleaner and easier to read.


# 1. Getting Started #######################################

# We'll need the purrr package for iteration functions
# and dplyr for data manipulation
library(purrr)
library(dplyr)

# We'll also use the built-in mtcars dataset
# This dataset contains information about 32 different car models
# Let's take a quick look at it
head(mtcars)
# You'll see columns like mpg (miles per gallon), cyl (cylinders), 
# hp (horsepower), etc.


# 2. What is Iteration? #######################################

# Iteration means repeating an operation on multiple items.
# 
# For example, imagine you want to calculate the mean of several columns
# in a dataset. Instead of writing:
#   mean(mtcars$mpg)
#   mean(mtcars$hp)
#   mean(mtcars$wt)
#   ... (and so on for each column)
#
# You can use iteration to apply the mean() function to each column automatically!
#
# The purrr package provides map() functions that make this easy.


# 3. Understanding map() #######################################

# map() applies a function to each element in a list or vector.
# The basic structure is:
#   map(.x = your_data, .f = your_function)
#
# - .x is the data you want to iterate over (a vector, list, or data frame columns)
# - .f is the function you want to apply to each element
#
# map() returns a list with the results


# 4. Your First map() #######################################

# Example: Calculate the mean of each numeric column in mtcars

# First, let's select just the numeric columns
numeric_cols = mtcars %>%
  select(where(is.numeric))

# Now use map() to calculate the mean of each column
means = map(.x = numeric_cols, .f = mean)

# Let's see what we got
means
# Output: A list where each element is the mean of one column
# $mpg: [1] 20.09062
# $cyl: [1] 6.1875
# $disp: [1] 230.7219
# ... and so on

# You can access individual results like this:
means$mpg
# Output: [1] 20.09062

means$hp
# Output: [1] 146.6875


# 5. map() with Different Functions #######################################

# You can use map() with any function!

# Example: Calculate the standard deviation of each column
standard_deviations = map(.x = numeric_cols, .f = sd)
standard_deviations

# Example: Find the minimum value in each column
minimums = map(.x = numeric_cols, .f = min)
minimums

# Example: Find the maximum value in each column
maximums = map(.x = numeric_cols, .f = max)
maximums


# 6. map() with Custom Functions #######################################

# You can also use map() with your own custom functions!

# Let's create a function that calculates the range (max - min)
calculate_range = function(x){
  max_value = max(x)
  min_value = min(x)
  range_value = max_value - min_value
  return(range_value)
}

# Now apply it to each column
ranges = map(.x = numeric_cols, .f = calculate_range)
ranges

# You can also write the function inline using ~ and . notation
# The ~ creates a function, and . represents each element
ranges = map(.x = numeric_cols, .f = ~ max(.) - min(.))
ranges


# 7. map() with Multiple Arguments #######################################

# Sometimes you want to pass additional arguments to your function.
# You can do this using additional arguments after .f

# Example: Calculate quantiles (percentiles) for each column
# The quantile() function takes a 'probs' argument to specify which quantiles
quantiles = map(.x = numeric_cols, .f = quantile, probs = c(0.25, 0.5, 0.75))
quantiles
# This calculates the 25th, 50th (median), and 75th percentiles for each column


# 8. map_dfr() - Combining Results into a Data Frame #######################################

# Often, you want your results in a nice data frame instead of a list.
# That's where map_dfr() comes in! The 'dfr' stands for "data frame rows."
# It combines all the results into a single data frame.

# Example: Calculate summary statistics for each column and combine into a data frame

# First, let's create a function that returns multiple statistics
get_summary_stats = function(x){
  data.frame(
    mean = mean(x),
    median = median(x),
    sd = sd(x),
    min = min(x),
    max = max(x)
  )
}

# Now apply it to each column using map_dfr()
# We need to also pass the column name, so let's modify our approach
summary_stats = map_dfr(.x = numeric_cols, .f = get_summary_stats, .id = "column")
summary_stats
# Output: A data frame with one row per column, showing all the statistics
# The .id = "column" argument creates a column showing which original column each row came from


# 9. A Better Approach: Using names() with map_dfr() #######################################

# Let's get the column names and create a more informative summary

# Create a function that takes both the data and the column name
get_summary_with_name = function(column_name, data){
  x = data[[column_name]]  # Get the column data
  data.frame(
    column = column_name,
    mean = mean(x),
    median = median(x),
    sd = sd(x),
    min = min(x),
    max = max(x)
  )
}

# Apply to each column name
column_names = names(numeric_cols)
summary_stats = map_dfr(.x = column_names, .f = get_summary_with_name, data = mtcars)
summary_stats
# Now we have a nice data frame with the column name and all statistics!


# 10. Practical Example: Analyzing Multiple Groups #######################################

# Let's use map_dfr() to analyze cars by number of cylinders

# Split the data by number of cylinders
cars_by_cyl = split(mtcars, mtcars$cyl)
# This creates a list where each element is a data frame of cars with that many cylinders

# Create a function to summarize each group
summarize_group = function(group_data){
  data.frame(
    cylinders = unique(group_data$cyl),
    n_cars = nrow(group_data),
    avg_mpg = mean(group_data$mpg),
    avg_hp = mean(group_data$hp),
    avg_wt = mean(group_data$wt)
  )
}

# Apply to each group
group_summaries = map_dfr(.x = cars_by_cyl, .f = summarize_group)
group_summaries
# Output: A data frame showing statistics for 4-cylinder, 6-cylinder, and 8-cylinder cars


# 11. map() vs. Loops #######################################

# You might be wondering: why use map() instead of a for loop?
# 
# Both work, but map() has advantages:
# 1. More concise and readable
# 2. Less error-prone (no need to manage indices)
# 3. Works well with the tidyverse style of coding
# 4. Automatically handles different data types
#
# However, for loops are still useful when you need:
# - Complex control flow (multiple conditions, breaks, etc.)
# - Operations that depend on previous iterations
# - When you're more comfortable with loops!

# Here's the same operation using a for loop (for comparison):
summary_list = list()
for(i in 1:length(column_names)){
  col_name = column_names[i]
  summary_list[[i]] = get_summary_with_name(col_name, mtcars)
}
summary_stats_loop = bind_rows(summary_list)
# This does the same thing, but map_dfr() is cleaner!


# 12. Other map() Variants #######################################

# purrr provides several variants of map() for different output types:
#
# - map() - returns a list
# - map_dbl() - returns a numeric vector (double)
# - map_int() - returns an integer vector
# - map_chr() - returns a character vector
# - map_lgl() - returns a logical (TRUE/FALSE) vector
# - map_dfr() - returns a data frame (combines rows)
# - map_dfc() - returns a data frame (combines columns)

# Example: Get means as a numeric vector instead of a list
mean_vector = map_dbl(.x = numeric_cols, .f = mean)
mean_vector
# Output: A named numeric vector
# mpg      cyl     disp       hp     drat       wt     qsec       vs       am     gear     carb 
# 20.09062  6.1875 230.7219 146.6875  3.596563  3.21725 17.84875  0.4375  0.40625  3.6875  2.8125


# 13. Cleaning Up #######################################

# Clear your environment
rm(list = ls())


# Conclusion #######################################

# Great! You've learned how to:
# - Use map() to apply functions to each element in a list or vector
# - Use map_dfr() to combine results into a data frame
# - Pass additional arguments to functions in map()
# - Use custom functions with map()
# - Understand when to use map() vs. loops
#
# The purrr package makes iteration cleaner and more powerful than traditional loops.
# Practice using map() and map_dfr() to make your code more elegant and efficient!

