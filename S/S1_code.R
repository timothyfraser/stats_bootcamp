# S1_code.R
# Workshop: Symbolic Calculus with Statistical Coding
# Prof: Timothy Fraser

# Sometimes in statistics and systems engineering, we know the mathematical 
# function for a probability density function (PDF), but we need to find the 
# cumulative distribution function (CDF) or reliability function (1 - CDF) 
# for projections and analysis.
#
# Instead of doing calculus by hand, we can use symbolic calculus in R to 
# automatically integrate or differentiate functions! This is especially 
# useful for reliability analysis, where we might want to project failure 
# probabilities over time (e.g., from time 1 to 1000).


# 1. Getting Started #######################################

# We'll need the mosaicCalc package for symbolic calculus
# install.packages("mosaicCalc")  # Uncomment to install
library(mosaicCalc)

# We'll also use dplyr and ggplot2 for data manipulation and visualization
library(dplyr)
library(ggplot2)


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

# We can write this as an R function:
pdf = function(x){
  -2/10^7 + 25/10^8*x + -45/10^12*x^2
}

# Let's test it with some values
pdf(2000)
pdf(3000)

# We can also apply it to a vector of values
pdf(c(2000, 3000, 4000))


# 4. Integrating PDF to Get CDF #######################################

# The cumulative distribution function (CDF) is the integral of the PDF.
# In R, we can use the `antiD()` function from mosaicCalc to compute 
# the anti-derivative (integral) of our PDF function.

# Compute the anti-derivative (integral) of pdf(x) with respect to x
cdf <- antiD(tilde = pdf(x) ~ x)

# Now cdf() is a function! We can use it just like any other function
cdf(2000)
cdf(3000)

# Let's compare: what's the cumulative probability up to 3000?
cdf(3000)

# We can apply it to multiple values
cdf(c(2000, 3000, 4000))


# 5. Differentiating CDF to Get PDF Back #######################################

# We can also go the other way! If we have a CDF, we can differentiate it 
# to get back the PDF. The `D()` function computes the derivative.

# Take the derivative of cdf(x) with respect to x
pdf2 <- D(tilde = cdf(x) ~ x)

# Let's verify that pdf2() gives us the same results as our original pdf()
pdf(2000)
pdf2(2000)

pdf(3000)
pdf2(3000)

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

# Define the PDF for failure times
failure_pdf = function(t){  0.01 * exp(-0.01*t)  }

# Integrate to get the CDF (probability of failure by time t)
failure_cdf = antiD(tilde = failure_pdf(t) ~ t)

# Calculate reliability function (probability of survival past time t)
reliability = function(t){  1 - failure_cdf(t)  }

# Now let's project reliability over time from 1 to 1000
time_points = seq(1, 1000, by = 10)
reliability_values = reliability(time_points)

# Create a data frame for visualization
reliability_data = data.frame(
  time = time_points,
  reliability = reliability_values
)

# Visualize the reliability curve
ggplot(reliability_data, aes(x = time, y = reliability)) +
  geom_line(color = "steelblue", size = 1) +
  theme_classic() +
  labs(
    x = "Time",
    y = "Reliability (Probability of Survival)",
    title = "Reliability Projection Over Time",
    subtitle = "Probability that component survives past time t"
  )

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
#    - Use ifelse() or other conditional logic when needed

# 3. Symbolic calculus is exact, but numerical evaluation may have rounding
#    - The functions created are symbolic, but evaluation is numerical
#    - This is usually fine for practical purposes


# 8. Cleaning Up #######################################

# Clear your environment when done
rm(list = ls())


# Conclusion #######################################

# Great! You've learned how to:
# - Use mosaicCalc's antiD() to integrate PDF functions and get CDF functions
# - Use mosaicCalc's D() to differentiate CDF functions and get PDF functions
# - Create reliability functions (1 - CDF) for projections
# - Project reliability over time periods (e.g., time 1 to 1000)
#
# Symbolic calculus in R is a powerful tool for systems engineering and 
# reliability analysis. When you know the mathematical form of a PDF, you can 
# automatically derive the CDF and reliability functions for projections and 
# simulations, without doing calculus by hand!

