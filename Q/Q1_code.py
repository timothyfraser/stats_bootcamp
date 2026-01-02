# Q1_code.py
# Workshop: Functions in Python
# Prof: Timothy Fraser

# We've learned how to use built-in Python functions like those in math and statistics
# to analyze distributions, but sometimes it's going to be more helpful to be 
# able to (A) do the math by hand or (B) code your own function to do it. 
# So, let's learn how in the world you do that!


# 1. Getting Started #######################################

# No packages to load! Keep going!

# 2. What is a Function? #######################################

# Functions are machines that do a specific calculation using an input 
# to produce a specific output.
# 
# Think of it like this:
# Input data (x) --> [Function does calculation] --> Output data (y)
#
# Below, we'll write an example function, called add(a, b).
# - This function takes two numeric values, a and b, as inputs, 
#   and adds them together.
# - Using def, we'll tell Python that our function contains two inputs, 
#   a and b.
# - Then, using indentation, we'll put the action we want Python to do.
# - The function can involve multiple operations inside it. 
#   But at the end, you need to return one final output, 
#   or Python will return None.


# 3. Creating Your First Function #######################################

# Make a function called 'add' that takes two inputs: a and b
def add(a, b):
    # Compute and directly return
    return a + b

# Now let's use it!
add(1, 2)
# Output: 3

# This also works - using return() explicitly (same as above)
def add(a, b):
    # Assign output to a temporary object
    output = a + b
    # Return the temporary object 'output'
    return output

# Use the function
add(1, 2)
# Output: 3


# 4. Functions with Default Inputs #######################################

# You can also assign default input values to your function. 
# Below, we write that by default, b = 2. 
# If we supply a different b, the default will get overwritten, 
# but otherwise, we won't need to supply b.

def add(a, b=2):
    return a + b

# Let's try it!

# See? I only need to write 'a' now (b defaults to 2)
add(1)
# Output: 3 (because 1 + 2 = 3)

# But if I write 'b' too...
add(1, 2)
# Output: 3

# And if I change 'b'...
add(1, 3)
# Output: 4
# It will adjust accordingly


# 5. More Complex Functions #######################################

# Functions can do more than just simple math!
# Let's create a function that calculates the mean of a list

def calculate_mean(numbers):
    # Sum all the numbers
    total = sum(numbers)
    # Count how many numbers there are
    count = len(numbers)
    # Calculate mean
    mean_value = total / count
    # Return the result
    return mean_value

# Try it out!
my_numbers = [1, 2, 3, 4, 5]
calculate_mean(my_numbers)
# Output: 3.0

# Compare to built-in function (using statistics module)
# Note: We're keeping it simple, but you could also use:
# import statistics
# statistics.mean(my_numbers)
# Output: 3.0 (same result!)


# 6. Functions with Multiple Steps #######################################

# Functions can contain multiple steps and operations

def square_and_add(x, y):
    # Step 1: Square the first number
    x_squared = x**2
    # Step 2: Square the second number
    y_squared = y**2
    # Step 3: Add them together
    result = x_squared + y_squared
    # Step 4: Return the result
    return result

# Try it!
square_and_add(3, 4)
# Output: 25 (because 3^2 + 4^2 = 9 + 16 = 25)


# 7. Functions with Conditional Logic #######################################

# Functions can also include if/else statements to make decisions

def is_positive(number):
    # Check if the number is greater than 0
    if number > 0:
        return "Yes, it's positive!"
    else:
        return "No, it's not positive."

# Try it!
is_positive(5)
# Output: "Yes, it's positive!"

is_positive(-3)
# Output: "No, it's not positive."

is_positive(0)
# Output: "No, it's not positive."


# 8. Cleaning Up #######################################

# Be sure to clear your environment when you're done practicing
# In Python, you can use globals().clear() to clear all global variables
# But be careful - this removes everything!

# globals().clear()  # Uncomment to clear all variables

# You can also remove specific objects using del
# del add, calculate_mean, square_and_add, is_positive


# Conclusion #######################################

# Great! You've learned how to:
# - Create your own functions using def
# - Use default values for function inputs
# - Write functions with multiple steps
# - Include conditional logic in functions
#
# Functions are powerful tools that let you reuse code and make 
# your analyses more organized and efficient. 
# Keep practicing, and you'll be a function-writing pro in no time!

