# S1_code.py
# Workshop: Symbolic Calculus with Statistical Coding
# Prof: Timothy Fraser

# Sometimes in statistics and systems engineering, we know the mathematical 
# function for a probability density function (PDF), but we need to find the 
# cumulative distribution function (CDF) or reliability function (1 - CDF) 
# for projections and analysis.
#
# Instead of doing calculus by hand, we can use symbolic calculus in Python 
# to automatically integrate or differentiate functions! This is especially 
# useful for reliability analysis, where we might want to project failure 
# probabilities over time (e.g., from time 1 to 1000).


# 1. Getting Started #######################################

# We'll need the sympy package for symbolic calculus
# !pip install sympy  # Uncomment to install

import sympy as sp  # Import sympy for symbolic calculus
import pandas as pd  # For data manipulation


# 2. What is Symbolic Calculus? #######################################

# Symbolic calculus means doing calculus (integration, differentiation) 
# on mathematical expressions symbolically, rather than numerically.
#
# For example:
# - If we have a PDF function f(x), we can integrate it to get the CDF F(x)
# - If we have a CDF function F(x), we can differentiate it to get the PDF f(x)
#
# This is powerful because:
# 1. We can work with known mathematical functions (e.g., from engineering models)
# 2. We can create functions for projections and simulations
# 3. We can analyze reliability over time periods


# 3. Creating a PDF Function #######################################

# Let's start with a simple example. Imagine we have a probability density 
# function (PDF) that describes the distribution of some variable.
#
# For this example, we'll use a polynomial function that approximates 
# a probability distribution:
# f(x) = -2/10^7 + 25x/10^8 - 45x^2/10^12

# We can write this as a Python function:
def pdf(x):
    return -2/10**7 + 25/10**8*x + -45/10**12*x**2

# Let's test it with some values
pdf(2000)
pdf(3000)

# We can also apply it to a list of values
[pdf(x) for x in [2000, 3000, 4000]]


# 4. Integrating PDF to Get CDF #######################################

# The cumulative distribution function (CDF) is the integral of the PDF.
# In Python, we can use sympy's `integrate()` function to compute 
# the integral of our PDF function symbolically.

# First, we need to define x as a symbolic variable
x = sp.symbols('x')

# Define the PDF as a symbolic expression
pdf_expr = -2/10**7 + 25/10**8*x + -45/10**12*x**2

# Integrate the PDF with respect to x to get the CDF
cdf_expr = sp.integrate(pdf_expr, x)

# Now we have a symbolic CDF expression! Let's see it
print("CDF expression:", cdf_expr)

# To evaluate the CDF at specific values, we substitute and evaluate
cdf_value_2000 = cdf_expr.subs(x, 2000).evalf()
cdf_value_3000 = cdf_expr.subs(x, 3000).evalf()

print("CDF at 2000:", cdf_value_2000)
print("CDF at 3000:", cdf_value_3000)

# We can create a function that evaluates the CDF for any value
def cdf(x_val):
    return float(cdf_expr.subs(x, x_val).evalf())

# Now we can use it like a regular function
cdf(2000)
cdf(3000)
cdf(4000)

# Or evaluate for multiple values at once
[cdf(val) for val in [2000, 3000, 4000]]


# 5. Differentiating CDF to Get PDF Back #######################################

# We can also go the other way! If we have a CDF, we can differentiate it 
# to get back the PDF. The `sp.diff()` function computes the derivative.

# Take the derivative of cdf_expr with respect to x
pdf2_expr = sp.diff(cdf_expr, x)

# Let's see the derivative
print("PDF from derivative:", pdf2_expr)

# Verify that pdf2_expr gives us the same results as our original pdf_expr
# They should be the same (or equivalent after simplification)
print("Original PDF:", pdf_expr)
print("PDF from derivative:", pdf2_expr.simplify())

# Let's verify numerically
pdf(2000)
float(pdf2_expr.subs(x, 2000).evalf())

pdf(3000)
float(pdf2_expr.subs(x, 3000).evalf())

# They should be the same! This confirms that integration and differentiation 
# are inverse operations.


# 6. Reliability Analysis: A Practical Application #######################################

# A common application in systems engineering is reliability analysis.
# If we know the PDF of failure times, we can:
# 1. Integrate to get the CDF (probability of failure by time t)
# 2. Calculate reliability = 1 - CDF (probability of survival past time t)
# 3. Project reliability over time periods

# Example: Let's say we have a PDF for component failure times
# f(t) = 0.01 * exp(-0.01*t)  (an exponential distribution)

# Define t as a symbolic variable
t = sp.symbols('t')

# Define the PDF for failure times as a symbolic expression
failure_pdf_expr = 0.01 * sp.exp(-0.01*t)

# Integrate to get the CDF (probability of failure by time t)
failure_cdf_expr = sp.integrate(failure_pdf_expr, t)

# Note: The indefinite integral needs a constant. For a proper CDF starting at 0,
# we typically evaluate from 0 to t. Let's do a definite integral:
failure_cdf_expr = sp.integrate(failure_pdf_expr, (t, 0, t))

# Create a function to evaluate the CDF
def failure_cdf(t_val):
    return float(failure_cdf_expr.subs(t, t_val).evalf())

# Calculate reliability function (probability of survival past time t)
def reliability(t_val):
    return 1 - failure_cdf(t_val)

# Now let's project reliability over time from 1 to 1000
time_points = list(range(1, 1001, 10))
reliability_values = [reliability(tp) for tp in time_points]

# Create a data frame for visualization
reliability_data = pd.DataFrame({
    'time': time_points,
    'reliability': reliability_values
})

# Note: For visualization, you would typically use plotnine or matplotlib
# Here's a simple text-based view of the data
print(reliability_data.head(10))

# What's the reliability at time 100?
reliability(100)

# What's the reliability at time 500?
reliability(500)


# 7. Practical Tips #######################################

# 1. Always check your functions work as expected
#    - Test with known values
#    - Verify that CDF(0) = 0 and CDF(infinity) = 1 (for proper PDFs)

# 2. Be careful with the domain of your functions
#    - Some functions are only valid for certain ranges
#    - Use conditional logic (if/else) when needed

# 3. Symbolic calculus is exact, but numerical evaluation may have rounding
#    - The expressions created are symbolic, but evaluation is numerical
#    - Use .evalf() to get floating point results
#    - This is usually fine for practical purposes


# 8. Cleaning Up #######################################

# Clear your environment when done
# In Python, you can use globals().clear() but be careful!
# It's often better to just remove specific variables

# For this script, we'll just note that variables remain in memory
# In practice, you might want to organize your code into functions
# or use a notebook environment where you can clear cells individually


# Conclusion #######################################

# Great! You've learned how to:
# - Use sympy's integrate() to integrate PDF functions and get CDF functions
# - Use sympy's diff() to differentiate CDF functions and get PDF functions
# - Create reliability functions (1 - CDF) for projections
# - Project reliability over time periods (e.g., time 1 to 1000)
#
# Symbolic calculus in Python is a powerful tool for systems engineering and 
# reliability analysis. When you know the mathematical form of a PDF, you can 
# automatically derive the CDF and reliability functions for projections and 
# simulations, without doing calculus by hand!

