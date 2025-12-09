# Workshop: Asynchronous Callbacks and Timeouts in R
# Prof: Timothy Fraser

# Sometimes you want functions to run in the background (asynchronously) 
# or you want to set a time limit on how long a function can run.
# This is especially useful when:
# - Processing large datasets
# - Making API calls that might be slow
# - Running computations that might hang
# - Running multiple operations in parallel
#
# In this workshop, we'll learn how to implement asynchronous callbacks
# and timeouts in R!


# 1. Getting Started #######################################

# We'll need several packages for asynchronous operations and timeouts
library(dplyr)      # For data manipulation (filter, etc.)
library(future)     # For asynchronous/parallel execution
library(later)      # For scheduling async callbacks
library(R.utils)    # For timeout functionality

# We'll use the built-in mtcars dataset for examples
head(mtcars)


# 2. What are Asynchronous Callbacks? #######################################

# Asynchronous (async) operations let your code continue running
# while a function executes in the background. When the function finishes,
# it "calls back" to let you know it's done.
#
# Think of it like ordering food at a restaurant:
# - You place your order (start async operation)
# - You can do other things while waiting (code continues)
# - The waiter brings your food when ready (callback executes)
#
# This is different from synchronous code, where you wait for each
# operation to finish before moving to the next one.


# 3. Setting Up Future Plans #######################################

# The `future` package lets us run code asynchronously.
# First, we need to set a "plan" that tells R how to execute futures.

# Plan: sequential (default - runs one at a time, not async)
plan(sequential)
# This is synchronous - code runs in order

# Plan: multisession (runs in separate R sessions - truly async)
plan(multisession, workers = 2)
# This allows code to run in parallel/async

# Plan: multicore (runs on multiple CPU cores - faster but not available on Windows)
# plan(multicore, workers = 2)  # Uncomment on Linux/Mac

# For this tutorial, we'll use multisession which works everywhere


# 4. Creating Asynchronous Functions with Futures #######################################

# A "future" is a promise that code will run and return a value.
# You can start a future, do other work, then get the result later.

# Example: Create a slow function that simulates processing
slow_calculation = function(data, delay_seconds = 2){
  # Simulate a slow operation by waiting
  Sys.sleep(delay_seconds)
  # Do some calculation
  result = mean(data) * 2
  return(result)
}

# Run it synchronously (we wait for it)
start_time = Sys.time()
result1 = slow_calculation(mtcars$mpg, delay_seconds = 2)
end_time = Sys.time()
cat("Synchronous took:", end_time - start_time, "seconds\n")

# Now run it asynchronously using future()
start_time = Sys.time()
future_result = future({
  slow_calculation(mtcars$mpg, delay_seconds = 2)
})
# Notice: This returns immediately! The calculation is running in the background.

# Do other work while it runs...
cat("I can do other things while the future runs!\n")
other_work = sum(mtcars$hp)
cat("Sum of horsepower:", other_work, "\n")

# Now get the result (this will wait if not ready yet)
result2 = value(future_result)
end_time = Sys.time()
cat("Asynchronous took:", end_time - start_time, "seconds\n")
# The total time is similar, but we did other work during the wait!


# 5. Asynchronous Callbacks with later() #######################################

# The `later` package lets us schedule functions to run asynchronously.
# A callback is a function that runs after a delay or when triggered.

# Example: Process data asynchronously, then run a callback
process_data_async = function(data_column, callback_function){
  # Create a future that processes the data
  future_result = future({
    # Simulate processing time
    Sys.sleep(1)
    # Calculate mean
    mean_value = mean(data_column)
    return(mean_value)
  })
  
  # Schedule a callback to run when we get the result
  # The callback will execute after the future completes
  later(function() {
    result = value(future_result)
    # Run the user's callback function
    callback_function(result)
  }, delay = 1.1)  # Slightly longer than the future's sleep time
  
  return(future_result)
}

# Define a callback function
print_result = function(result) {
  cat("Processing complete! Mean value:", result, "\n")
  cat("Doubled value:", result * 2, "\n")
}

# Use it
future_result = process_data_async(mtcars$mpg, print_result)
# The callback will execute when processing finishes
# Note: You may need to run run_now() to execute scheduled callbacks immediately


# Cleaning Up #######################################

# Reset the future plan
plan(sequential)

# Clear your environment
rm(list = ls())
