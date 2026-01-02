# Q3_code.py
# Workshop: Iteration with map() in Python
# Prof: Timothy Fraser

# Now that we know how to write functions and use loops, let's learn a more 
# elegant way to apply functions to multiple items: Python's built-in map() function!
# 
# Python's map() function provides powerful tools for iteration (repeating operations).
# Instead of writing for loops, we can use map() to apply a function
# to each element in a list or sequence. This is often cleaner and easier to read.


# 1. Getting Started #######################################

# We'll need pandas for data manipulation
import pandas as pd

# We'll create a sample dataset similar to mtcars
# This dataset contains information about different car models
# Let's create a simple version with key columns
mtcars = pd.DataFrame({
    'mpg': [21.0, 21.0, 22.8, 21.4, 18.7, 18.1, 14.3, 24.4, 22.8, 19.2, 17.8, 16.4, 17.3, 15.2, 10.4, 10.4, 14.7, 32.4, 30.4, 33.9, 21.5, 15.5, 15.2, 13.3, 19.2, 27.3, 26.0, 30.4, 15.8, 19.7, 15.0, 21.4],
    'cyl': [6, 6, 4, 6, 8, 6, 8, 4, 4, 6, 6, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 8, 6, 8, 4],
    'disp': [160.0, 160.0, 108.0, 258.0, 360.0, 225.0, 360.0, 146.7, 140.8, 167.6, 167.6, 275.8, 275.8, 275.8, 472.0, 460.0, 440.0, 78.7, 75.7, 71.1, 120.1, 318.0, 304.0, 350.0, 400.0, 79.0, 120.3, 95.1, 351.0, 145.0, 301.0, 121.0],
    'hp': [110, 110, 93, 110, 175, 105, 245, 62, 95, 123, 123, 180, 180, 180, 205, 215, 230, 66, 52, 65, 97, 150, 150, 245, 175, 66, 91, 113, 264, 175, 335, 109],
    'drat': [3.90, 3.90, 3.85, 3.08, 3.15, 2.76, 3.21, 3.69, 3.92, 3.92, 3.92, 3.07, 3.07, 3.07, 2.93, 3.00, 3.23, 4.08, 4.93, 4.22, 3.70, 2.76, 3.15, 3.73, 3.08, 4.08, 4.43, 3.77, 4.22, 3.62, 3.54, 4.11],
    'wt': [2.620, 2.875, 2.320, 3.215, 3.440, 3.460, 3.570, 3.190, 3.150, 3.440, 3.440, 4.070, 3.730, 3.780, 5.250, 5.424, 5.345, 2.200, 1.615, 1.835, 2.465, 3.520, 3.435, 3.840, 3.845, 1.935, 2.140, 1.513, 3.170, 2.770, 3.570, 2.780],
    'qsec': [16.46, 17.02, 18.61, 19.44, 17.02, 20.22, 15.84, 20.00, 22.90, 18.30, 18.90, 17.40, 17.60, 18.00, 17.98, 17.82, 17.42, 19.47, 18.52, 19.90, 20.01, 16.87, 17.30, 15.41, 17.05, 18.90, 16.70, 16.90, 14.50, 15.50, 14.60, 18.60],
    'vs': [0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    'am': [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    'gear': [4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3, 4, 5, 5, 5, 5, 5, 4],
    'carb': [4, 4, 1, 1, 2, 1, 4, 2, 2, 4, 4, 3, 3, 3, 4, 4, 4, 1, 2, 1, 1, 2, 2, 4, 2, 1, 2, 2, 4, 6, 8, 2]
})

# Let's take a quick look at it
print(mtcars.head())
# You'll see columns like mpg (miles per gallon), cyl (cylinders), 
# hp (horsepower), etc.


# 2. What is Iteration? #######################################

# Iteration means repeating an operation on multiple items.
# 
# For example, imagine you want to calculate the mean of several columns
# in a dataset. Instead of writing:
#   mtcars['mpg'].mean()
#   mtcars['hp'].mean()
#   mtcars['wt'].mean()
#   ... (and so on for each column)
#
# You can use iteration to apply the mean() function to each column automatically!
#
# Python's built-in map() function makes this easy.


# 3. Understanding map() #######################################

# map() applies a function to each element in a sequence (list, tuple, etc.).
# The basic structure is:
#   map(function, sequence)
#
# - function is the function you want to apply to each element
# - sequence is the data you want to iterate over (a list, tuple, etc.)
#
# map() returns a map object (an iterator) with the results
# You can convert it to a list to see the results


# 4. Your First map() #######################################

# Example: Calculate the mean of each numeric column in mtcars

# First, let's select just the numeric columns
numeric_cols = mtcars.select_dtypes(include=['number'])

# Now use map() to calculate the mean of each column
# We'll iterate over the column names and apply mean to each column
column_names = numeric_cols.columns
means = {col: numeric_cols[col].mean() for col in column_names}

# Let's see what we got
print(means)
# Output: A dictionary where each key is a column name and value is the mean
# {'mpg': 20.090625, 'cyl': 6.1875, 'disp': 230.721875, ...}

# You can access individual results like this:
means['mpg']
# Output: 20.090625

means['hp']
# Output: 146.6875

# Alternative: Using map() with a list of column names
# This is closer to the R purrr style
def get_mean(col_name):
    return numeric_cols[col_name].mean()

means_list = list(map(get_mean, column_names))
# This gives a list of means (but loses column names)

# Better: Using dictionary comprehension (Pythonic way)
means = {col: numeric_cols[col].mean() for col in column_names}


# 5. map() with Different Functions #######################################

# You can use map() with any function!

# Example: Calculate the standard deviation of each column
standard_deviations = {col: numeric_cols[col].std() for col in column_names}
print(standard_deviations)

# Example: Find the minimum value in each column
minimums = {col: numeric_cols[col].min() for col in column_names}
print(minimums)

# Example: Find the maximum value in each column
maximums = {col: numeric_cols[col].max() for col in column_names}
print(maximums)


# 6. map() with Custom Functions #######################################

# You can also use map() with your own custom functions!

# Let's create a function that calculates the range (max - min)
def calculate_range(x):
    max_value = max(x)
    min_value = min(x)
    range_value = max_value - min_value
    return range_value

# Now apply it to each column using map()
ranges = {col: calculate_range(numeric_cols[col]) for col in column_names}
print(ranges)

# You can also write the function inline using a lambda function
# Lambda functions are anonymous functions defined with lambda
ranges = {col: (lambda x: max(x) - min(x))(numeric_cols[col]) for col in column_names}
print(ranges)

# Or more simply:
ranges = {col: numeric_cols[col].max() - numeric_cols[col].min() for col in column_names}
print(ranges)


# 7. map() with Multiple Arguments #######################################

# Sometimes you want to pass additional arguments to your function.
# You can do this by creating a wrapper function or using lambda with additional args

# Example: Calculate quantiles (percentiles) for each column
# The quantile() method in pandas takes a 'q' argument to specify which quantiles
def get_quantiles(col_name, probs):
    return numeric_cols[col_name].quantile(q=probs)

# Apply to each column
quantiles = {col: get_quantiles(col, [0.25, 0.5, 0.75]) for col in column_names}
print(quantiles)
# This calculates the 25th, 50th (median), and 75th percentiles for each column


# 8. Combining Results into a DataFrame #######################################

# Often, you want your results in a nice data frame instead of a dictionary.
# We can create a DataFrame from a list of dictionaries.

# Example: Calculate summary statistics for each column and combine into a data frame

# First, let's create a function that returns multiple statistics
def get_summary_stats(col_name):
    col_data = numeric_cols[col_name]
    return {
        'column': col_name,
        'mean': col_data.mean(),
        'median': col_data.median(),
        'sd': col_data.std(),
        'min': col_data.min(),
        'max': col_data.max()
    }

# Now apply it to each column using map() and convert to DataFrame
summary_list = [get_summary_stats(col) for col in column_names]
summary_stats = pd.DataFrame(summary_list)
print(summary_stats)
# Output: A data frame with one row per column, showing all the statistics


# 9. A Better Approach: Using column names directly #######################################

# Let's create a more informative summary using the column names directly

# Create a function that takes the column name and returns summary stats
def get_summary_with_name(column_name):
    col_data = numeric_cols[column_name]
    return {
        'column': column_name,
        'mean': col_data.mean(),
        'median': col_data.median(),
        'sd': col_data.std(),
        'min': col_data.min(),
        'max': col_data.max()
    }

# Apply to each column name
summary_stats = pd.DataFrame([get_summary_with_name(col) for col in column_names])
print(summary_stats)
# Now we have a nice data frame with the column name and all statistics!


# 10. Practical Example: Analyzing Multiple Groups #######################################

# Let's analyze cars by number of cylinders

# Split the data by number of cylinders using groupby
cars_by_cyl = {cyl: group for cyl, group in mtcars.groupby('cyl')}
# This creates a dictionary where each key is a cylinder count and value is a DataFrame

# Create a function to summarize each group
def summarize_group(group_data):
    return {
        'cylinders': group_data['cyl'].iloc[0],  # Get unique value (all same in group)
        'n_cars': len(group_data),
        'avg_mpg': group_data['mpg'].mean(),
        'avg_hp': group_data['hp'].mean(),
        'avg_wt': group_data['wt'].mean()
    }

# Apply to each group
group_summaries = pd.DataFrame([summarize_group(group) for group in cars_by_cyl.values()])
print(group_summaries)
# Output: A data frame showing statistics for 4-cylinder, 6-cylinder, and 8-cylinder cars


# 11. map() vs. Loops #######################################

# You might be wondering: why use map() or list comprehensions instead of a for loop?
# 
# Both work, but map() and list comprehensions have advantages:
# 1. More concise and readable
# 2. Less error-prone (no need to manage indices)
# 3. More Pythonic (idiomatic Python style)
# 4. Automatically handles different data types
#
# However, for loops are still useful when you need:
# - Complex control flow (multiple conditions, breaks, etc.)
# - Operations that depend on previous iterations
# - When you're more comfortable with loops!

# Here's the same operation using a for loop (for comparison):
summary_list = []
for col_name in column_names:
    summary_list.append(get_summary_with_name(col_name))
summary_stats_loop = pd.DataFrame(summary_list)
# This does the same thing, but list comprehensions are cleaner!


# 12. Other Iteration Methods #######################################

# Python provides several ways to iterate and apply functions:
#
# - map() - returns a map object (iterator)
# - List comprehensions - returns a list directly (often preferred in Python)
# - Dictionary comprehensions - returns a dictionary
# - Generator expressions - memory-efficient iteration
#
# Example: Get means as a dictionary (we already did this above)
mean_dict = {col: numeric_cols[col].mean() for col in column_names}
# Wait, that's a set comprehension! For dict, we need:
mean_dict = {col: numeric_cols[col].mean() for col in column_names}
print(mean_dict)
# Output: A dictionary with column names as keys and means as values


# 13. Cleaning Up #######################################

# Clear your environment
# In Python, you can use globals().clear() to clear all global variables
# But be careful - this removes everything!

# globals().clear()  # Uncomment to clear all variables


# Conclusion #######################################

# Great! You've learned how to:
# - Use map() and list comprehensions to apply functions to each element
# - Combine results into a DataFrame
# - Pass additional arguments to functions in iterations
# - Use custom functions with map() and comprehensions
# - Understand when to use map() vs. loops
#
# Python's map() function and list comprehensions make iteration cleaner and more powerful than traditional loops.
# Practice using map() and comprehensions to make your code more elegant and efficient!

