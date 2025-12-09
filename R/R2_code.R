# Workshop: Loops in R
# Prof: Timothy Fraser

# Sometimes you want to repeat the same action multiple times.
# Instead of writing the same code over and over, you can use loops!
# Loops let you repeat code automatically, which saves time and makes 
# your code cleaner and easier to read.


# 1. Getting Started #######################################

# No packages to load! All of this is built into R!


# 2. What is a Loop? #######################################

# A loop is a way to repeat code multiple times.
# Think of it like this: "For each item in a list, do this action."
# 
# There are two main types of loops in R:
# 1. for loops - repeat code a specific number of times
# 2. while loops - repeat code as long as a condition is true
#
# We'll focus on for loops first, as they're the most common.


# 3. Your First For Loop #######################################

# A for loop repeats code for each item in a sequence.
# The basic structure is:
# for(variable in sequence){
#   do something
# }

# Example: Print numbers 1 through 5
for(i in 1:5){
  print(i)
}
# Output:
# [1] 1
# [1] 2
# [1] 3
# [1] 4
# [1] 5

# What happened?
# - i is a variable that takes on each value in the sequence 1:5
# - First, i = 1, so it prints 1
# - Then, i = 2, so it prints 2
# - And so on, until i = 5


# 4. Looping Through a Vector #######################################

# You can loop through any vector (list of values)

# Example: Loop through a vector of town names
towns = c("Boston", "New York", "Los Angeles", "Chicago")

for(town in towns){
  print(town)
}
# Output:
# [1] "Boston"
# [1] "New York"
# [1] "Los Angeles"
# [1] "Chicago"

# Notice: the variable name (town) can be anything you want!
# It's just a placeholder that represents each item as we loop through.


# 5. Doing Calculations in Loops #######################################

# You can do calculations inside loops

# Example: Calculate the square of each number from 1 to 5
for(number in 1:5){
  squared = number^2
  print(squared)
}
# Output:
# [1] 1
# [1] 4
# [1] 9
# [1] 16
# [1] 25


# 6. Storing Results from Loops #######################################

# Often, you want to save the results from your loop.
# You can create an empty vector first, then fill it up.

# Example: Store squares in a new vector
squares = c()  # Start with an empty vector

for(number in 1:5){
  squared = number^2
  squares = c(squares, squared)  # Add the new value to the vector
}

# Now check what we stored
squares
# Output: [1]  1  4  9 16 25


# 7. A Better Way: Pre-allocate Space #######################################

# For better performance, you can create a vector with the right size first,
# then fill in each position.

# Example: Create a vector with 5 empty spots
results = numeric(5)  # Creates a vector of 5 zeros

# Now fill it in
for(i in 1:5){
  results[i] = i^2  # Put the square in position i
}

results
# Output: [1]  1  4  9 16 25


# 8. Nested Loops #######################################

# You can put loops inside other loops! This is called "nesting."

# Example: Create a multiplication table
for(i in 1:3){
  for(j in 1:3){
    product = i * j
    print(paste(i, "times", j, "equals", product))
  }
}
# Output:
# [1] "1 times 1 equals 1"
# [1] "1 times 2 equals 2"
# [1] "1 times 3 equals 3"
# [1] "2 times 1 equals 2"
# [1] "2 times 2 equals 4"
# [1] "2 times 3 equals 6"
# [1] "3 times 1 equals 3"
# [1] "3 times 2 equals 6"
# [1] "3 times 3 equals 9"

# What happened?
# - The outer loop (i) goes through 1, 2, 3
# - For each value of i, the inner loop (j) goes through 1, 2, 3
# - So we get all combinations: 1×1, 1×2, 1×3, 2×1, 2×2, 2×3, etc.


# 9. While Loops #######################################

# A while loop repeats code as long as a condition is true.
# Be careful! If the condition never becomes false, the loop runs forever!

# Example: Count up from 1 until we reach 5
counter = 1

while(counter <= 5){
  print(counter)
  counter = counter + 1  # Increase counter by 1
}
# Output:
# [1] 1
# [1] 2
# [1] 3
# [1] 4
# [1] 5

# What happened?
# - Start with counter = 1
# - Check: Is counter <= 5? Yes, so print 1 and add 1 to counter
# - Now counter = 2
# - Check: Is counter <= 5? Yes, so print 2 and add 1 to counter
# - Continue until counter = 6, then stop (because 6 <= 5 is false)


# 10. Breaking Out of Loops #######################################

# Sometimes you want to stop a loop early. You can use break.

# Example: Stop when we find the number 3
for(i in 1:10){
  print(i)
  if(i == 3){
    break  # Stop the loop immediately
  }
}
# Output:
# [1] 1
# [1] 2
# [1] 3
# (Stops here, even though we could go to 10)


# 11. Skipping Iterations #######################################

# You can skip to the next iteration using next.

# Example: Print only even numbers
for(i in 1:10){
  if(i %% 2 != 0){  # If i is odd (remainder when divided by 2 is not 0)
    next  # Skip to the next iteration
  }
  print(i)  # Only print if we didn't skip
}
# Output:
# [1] 2
# [1] 4
# [1] 6
# [1] 8
# [1] 10


# 12. Practical Example: Processing Data #######################################

# Let's use a loop to calculate statistics for multiple columns

# Create some sample data
data = data.frame(
  height = c(65, 70, 68, 72, 69),
  weight = c(150, 180, 160, 200, 170),
  age = c(25, 30, 28, 35, 32)
)

# Calculate the mean of each column using a loop
column_names = names(data)  # Get the column names

for(col in column_names){
  mean_value = mean(data[[col]])  # Calculate mean for this column
  print(paste("Mean of", col, ":", mean_value))
}
# Output:
# [1] "Mean of height : 68.8"
# [1] "Mean of weight : 172"
# [1] "Mean of age : 30"


# 13. Cleaning Up #######################################

# Clear your environment
rm(list = ls())


# Conclusion #######################################

# Great! You've learned how to:
# - Use for loops to repeat code
# - Loop through vectors and sequences
# - Store results from loops
# - Use nested loops
# - Use while loops
# - Break out of loops or skip iterations
#
# Loops are powerful tools for automating repetitive tasks.
# However, in R, there are often more efficient ways to do things
# (like using apply functions, which we'll learn about next!).
# But loops are still important to understand and use when needed.

