# Workshop: Functions in R
# Prof: Timothy Fraser

# We've learned how to use built-in R functions like dnorm() and pnorm() 
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
# - Using function(), we'll tell R that our function contains two inputs, 
#   a and b.
# - Then, using { ... }, we'll put the action we want R to do in there.
# - The function can involve multiple operations inside it. 
#   But at the end, you need to print one final output, 
#   or put return() around your output.


# 3. Creating Your First Function #######################################

# Make a function called 'add' that takes two inputs: a and b
add = function(a, b){
  # Compute and directly output
  a + b 
}

# Now let's use it!
add(1, 2)
# Output: 3

# This also works - using return() explicitly
add = function(a, b){
  # Assign output to a temporary object
  output = a + b
  # Return the temporary object 'output'
  return(output)
}

# Use the function
add(1, 2)
# Output: 3


# 4. Functions with Default Inputs #######################################

# You can also assign default input values to your function. 
# Below, we write that by default, b = 2. 
# If we supply a different b, the default will get overwritten, 
# but otherwise, we won't need to supply b.

add <- function(a, b = 2){
  a + b
}

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
# Let's create a function that calculates the mean of a vector

calculate_mean = function(numbers){
  # Sum all the numbers
  total = sum(numbers)
  # Count how many numbers there are
  count = length(numbers)
  # Calculate mean
  mean_value = total / count
  # Return the result
  return(mean_value)
}

# Try it out!
my_numbers <- c(1, 2, 3, 4, 5)
calculate_mean(my_numbers)
# Output: 3

# Compare to built-in function
mean(my_numbers)
# Output: 3 (same result!)


# 6. Functions with Multiple Steps #######################################

# Functions can contain multiple steps and operations

square_and_add = function(x, y){
  # Step 1: Square the first number
  x_squared = x^2
  # Step 2: Square the second number
  y_squared = y^2
  # Step 3: Add them together
  result = x_squared + y_squared
  # Step 4: Return the result
  return(result)
}

# Try it!
square_and_add(3, 4)
# Output: 25 (because 3^2 + 4^2 = 9 + 16 = 25)


# 7. Functions with Conditional Logic #######################################

# Functions can also include if/else statements to make decisions

is_positive = function(number){
  # Check if the number is greater than 0
  if(number > 0){
    return("Yes, it's positive!")
  } else {
    return("No, it's not positive.")
  }
}

# Try it!
is_positive(5)
# Output: "Yes, it's positive!"

is_positive(-3)
# Output: "No, it's not positive."

is_positive(0)
# Output: "No, it's not positive."


# 8. Cleaning Up #######################################

# Be sure to clear your environment when you're done practicing
rm(list = ls())

# You can also remove specific objects
# remove(add, calculate_mean, square_and_add, is_positive)


# Conclusion #######################################

# Great! You've learned how to:
# - Create your own functions using function()
# - Use default values for function inputs
# - Write functions with multiple steps
# - Include conditional logic in functions
#
# Functions are powerful tools that let you reuse code and make 
# your analyses more organized and efficient. 
# Keep practicing, and you'll be a function-writing pro in no time!

