# Q4_code.py
# Workshop: Asynchronous Callbacks and Timeouts in Python
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
# and timeouts in Python!


# 1. Getting Started #######################################

# We'll need several modules for asynchronous operations and timeouts
import pandas as pd  # For data manipulation
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError  # For async/parallel execution
import time  # For sleep and timing
import threading  # For callbacks and timers

# We'll use a sample dataset for examples
# Let's create a simple dataset similar to mtcars
mtcars = pd.DataFrame({
    'mpg': [21.0, 21.0, 22.8, 21.4, 18.7, 18.1, 14.3, 24.4, 22.8, 19.2, 17.8, 16.4, 17.3, 15.2, 10.4, 10.4, 14.7, 32.4, 30.4, 33.9, 21.5, 15.5, 15.2, 13.3, 19.2, 27.3, 26.0, 30.4, 15.8, 19.7, 15.0, 21.4],
    'hp': [110, 110, 93, 110, 175, 105, 245, 62, 95, 123, 123, 180, 180, 180, 205, 215, 230, 66, 52, 65, 97, 150, 150, 245, 175, 66, 91, 113, 264, 175, 335, 109]
})

print(mtcars.head())


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


# 3. Setting Up Thread Pool Executor #######################################

# The `concurrent.futures` module lets us run code asynchronously.
# ThreadPoolExecutor runs functions in separate threads (good for I/O-bound tasks).
# ProcessPoolExecutor runs functions in separate processes (good for CPU-bound tasks).

# Create an executor with 2 worker threads
executor = ThreadPoolExecutor(max_workers=2)
# This allows code to run in parallel/async


# 4. Creating Asynchronous Functions with Futures #######################################

# A "future" is a promise that code will run and return a value.
# You can start a future, do other work, then get the result later.

# Example: Create a slow function that simulates processing
def slow_calculation(data, delay_seconds=2):
    # Simulate a slow operation by waiting
    time.sleep(delay_seconds)
    # Do some calculation
    result = data.mean() * 2
    return result

# Run it synchronously (we wait for it)
start_time = time.time()
result1 = slow_calculation(mtcars['mpg'], delay_seconds=2)
end_time = time.time()
print(f"Synchronous took: {end_time - start_time:.2f} seconds")
print(f"Result: {result1}")


# Now run it asynchronously using submit()
future_result = executor.submit(slow_calculation, mtcars['mpg'], 5)
# Notice: This returns immediately! The calculation is running in the background.

# Do other work while it runs...
print("I can do other things while the future runs!")
other_work = mtcars['hp'].sum()
print(f"Sum of horsepower: {other_work}")

# Now get the result (this will wait if not ready yet)
result2 = future_result.result()  # This blocks until the result is ready
print(f"Async result: {result2}")


# 5. Asynchronous Callbacks with Threading #######################################

# We can schedule functions to run as callbacks when futures complete.
# A callback is a function that runs after a delay or when triggered.

# Example: Process data asynchronously, then run a callback
def process_data_async(data_column, callback_function, executor):
    # Create a future that processes the data
    future_result = executor.submit(lambda: process_data(data_column))
    
    # Define a function to check and run callback when ready
    def check_and_callback():
        try:
            result = future_result.result(timeout=10)  # Wait up to 10 seconds
            # Run the user's callback function
            callback_function(result)
        except Exception as e:
            print(f"Error in callback: {e}")
    
    # Start a thread that will check when ready
    callback_thread = threading.Thread(target=check_and_callback)
    callback_thread.start()
    
    return future_result

def process_data(data_column):
    # Simulate processing time
    time.sleep(1)
    # Calculate mean
    mean_value = data_column.mean()
    return mean_value

# Define a callback function
def print_result(result):
    print(f"Processing complete! Mean value: {result}")
    print(f"Doubled value: {result * 2}")

# Use it
future_result = process_data_async(mtcars['mpg'], print_result, executor)
# The callback will execute when processing finishes
# Note: You may need to wait a moment for the callback to execute
time.sleep(2)  # Give it time to complete


# 6. Setting Timeouts #######################################

# Sometimes you want to limit how long a function can run.
# You can use the timeout parameter in result() to set a maximum wait time.

# Example: Set a timeout on a slow operation
def very_slow_calculation(data, delay_seconds=10):
    time.sleep(delay_seconds)
    return data.mean()

# Submit the slow calculation
future_slow = executor.submit(very_slow_calculation, mtcars['mpg'], 10)

try:
    # Try to get result with a 3-second timeout
    result = future_slow.result(timeout=3)
    print(f"Result: {result}")
except FuturesTimeoutError:
    print("Operation timed out! The function is still running in the background.")
    # You can cancel it if needed
    future_slow.cancel()
    print("Future cancelled.")


# 7. Running Multiple Operations in Parallel #######################################

# You can run multiple operations at the same time!

# Example: Calculate means for multiple columns in parallel
def calculate_mean_for_column(column_name, data):
    time.sleep(0.5)  # Simulate some processing time
    return {column_name: data[column_name].mean()}

# Submit multiple futures
futures = []
for col in ['mpg', 'hp']:
    future = executor.submit(calculate_mean_for_column, col, mtcars)
    futures.append((col, future))

# Do other work while they run...
print("Doing other work while calculations run...")

# Collect results when ready
results = {}
for col, future in futures:
    result = future.result()  # This will wait for each to complete
    results.update(result)

print("All results:", results)


# 8. Using Context Manager for Clean Resource Management #######################################

# It's good practice to use a context manager (with statement) 
# to ensure the executor is properly cleaned up.

# Example: Using executor as a context manager
def run_async_example():
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Submit work
        future = executor.submit(slow_calculation, mtcars['mpg'], 2)
        
        # Do other work
        print("Working on other things...")
        
        # Get result
        result = future.result()
        print(f"Got result: {result}")
    # Executor is automatically shut down here

run_async_example()


# 9. Practical Example: Processing Multiple Datasets #######################################

# Let's use async operations to process multiple datasets in parallel

def process_dataset(dataset_name, data):
    # Simulate processing
    time.sleep(1)
    return {
        'dataset': dataset_name,
        'mean': data.mean(),
        'count': len(data)
    }

# Process multiple columns as if they were separate datasets
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(process_dataset, 'mpg', mtcars['mpg']),
        executor.submit(process_dataset, 'hp', mtcars['hp'])
    ]
    
    # Collect all results
    results = [future.result() for future in futures]
    results_df = pd.DataFrame(results)
    print(results_df)


# Cleaning Up #######################################

# If you created an executor outside a context manager, shut it down
executor.shutdown(wait=True)  # wait=True means wait for all tasks to complete

# Clear your environment
# globals().clear()  # Uncomment to clear all variables


# Conclusion #######################################

# Great! You've learned how to:
# - Use ThreadPoolExecutor to run functions asynchronously
# - Get results from futures
# - Set timeouts on operations
# - Run multiple operations in parallel
# - Use callbacks to handle completed operations
# - Properly manage executor resources
#
# Asynchronous programming is powerful for improving performance
# when you have I/O-bound operations or want to run multiple tasks in parallel.
# Practice using these tools to make your code more efficient!

