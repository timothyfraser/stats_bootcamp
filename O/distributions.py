# distributions.py
# Installation requirements
# !pip install scipy # import scipy functions
# !pip install plotnine # import visualization functions
# from scipy.stats import norm, expon, gamma, weibull_min, poisson, uniform, binom

# Simple visualization #############################

# Want to make a quick histogram?
def hist(x):
  """
  Make a quick histogram, in syntax matching the method in R.
  
  Parameters:
    x: a pandas Series of values to be turned into a histogram
    
  Returns: 
    figure: a ggplot figure object.
  """
  from plotnine import ggplot, geom_histogram, aes
  output = ggplot(aes(x = x)) + geom_histogram()
  return output

# Skewness & Kurtosis ##############################
def skewness(x):
    from pandas import Series
    x = Series(x)
    diff = x - x.mean()
    n = len(x) - 1
    sigma = x.std()
    output = sum(diff**3) / (n * sigma**3)
    return output

def kurtosis(x):
    from pandas import Series
    x = Series(x)
    diff = x - x.mean()
    n = len(x) - 1
    sigma = x.std()
    output = sum(diff**4) / (n * sigma**4)
    return output


# Probability Distribution Functions ####################

def seq(from_, to, length_out=None, by=None):
    """
    Generate a sequence of numbers, similar to R's `seq` function.

    This function generates a sequence from `from_` to `to`, with either a specified length (`length_out`) or step size (`by`).
    You can specify only one of `length_out` or `by` to define the sequence.

    Parameters:
    -----------
    from_ : float
        The starting value of the sequence.
    to : float
        The ending value of the sequence.
    length_out : int, optional, default=None
        The number of elements to generate in the sequence. Exactly one of `length_out` or `by` must be specified.
    by : float, optional, default=None
        The step size between consecutive values in the sequence. Exactly one of `length_out` or `by` must be specified.

    Returns:
    --------
    pandas.Series
        A Series containing the sequence of values, either generated based on the specified length or step size.

    Raises:
    -------
    ValueError:
        - If both `length_out` and `by` are provided, or if neither is provided.
        - If `length_out` is less than 1.
        - If `by` is zero.

    Notes:
    ------
    - If `length_out` is provided, the function will generate a sequence with exactly that many points, distributed evenly between `from_` and `to`.
    - If `by` is provided, the function will generate a sequence with a step size of `by`, starting from `from_` and ending at or before `to`.
    - The sequence is generated using `pandas.Series` for flexibility and efficient operations.

    Examples:
    ---------
    seq(0, 1, length_out=10)
    seq(-3, 1, by=0.1)
    """
    import pandas as pd
    
    if length_out is not None and by is not None:
        raise ValueError("Only one of `length_out` or `by` should be provided.")
    
    # Generate sequence based on `length_out`
    if length_out is not None:
        if length_out < 1:
            raise ValueError("`length_out` must be at least 1.")
        sequence = pd.Series(pd.Series(range(length_out)).apply(lambda x: from_ + (to - from_) * x / (length_out - 1)))
    
    # Generate sequence based on `by`
    elif by is not None:
        if by == 0:
            raise ValueError("`by` must be non-zero.")
        sequence = pd.Series(range(int((to - from_) / by) + 1)).apply(lambda x: from_ + x * by)
    
    else:
        raise ValueError("Either `length_out` or `by` must be provided.")
    
    return sequence


def density(x):
    """
    Estimate the probability density function (PDF) of a given dataset using Gaussian Kernel Density Estimation (KDE).

    Parameters:
    -----------
    x : array-like
        A list or array of data points for which the density is to be estimated.

    Returns:
    --------
    scipy.stats.gaussian_kde
        A Gaussian KDE model that can be used to evaluate the density at different points.

    Notes:
    ------
    This function uses `scipy.stats.gaussian_kde` to estimate the kernel density of the input data.
    The resulting model can be evaluated at any point to estimate the density at that point.
    """
    from scipy.stats import gaussian_kde as density
    output = density(x)
    return output


def tidy_density(model, n=1000):
    """
    Estimate the probability density function (PDF) over a range of values using a Gaussian KDE model and return it in a tidy format.

    Parameters:
    -----------
    model : callable
        A kernel density estimate model (e.g., the result from the `density` function) that can evaluate density at given points.
    n : int, optional, default=1000
        The number of points over which to estimate the density. The range of points is determined by the minimum and maximum of the dataset.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing two columns: 'x' (the values where density is evaluated) and 'y' (the corresponding density values).

    Notes:
    ------
    This function uses `numpy.linspace` to generate a range of values from the minimum to the maximum of the dataset,
    and then evaluates the density at those points using the provided model.
    The result is returned as a tidy DataFrame with 'x' and 'y' columns.
    """
    from numpy import linspace
    from pandas import Series, DataFrame
    values = linspace(start=model.dataset.min(), stop=model.dataset.max(), num=n)
    densities = model(values)
    output = DataFrame({'x': Series(values), 'y': Series(densities)})
    return output

def approxfun(data, fill_value='extrapolate', bounds_error=False):
    """
    Approximate a DataFrame of x and y data into a linear interpolation function.

    Parameters:
    -----------
    data : pandas.DataFrame
        A DataFrame containing the x and y values that need to be approximated.
        The DataFrame should have two columns, where one is labeled 'x' for the independent variable
        and the other is labeled 'y' for the dependent variable.
    fill_value : str or scalar, optional, default='extrapolate'
        Value used to fill in for missing data (i.e., when interpolating outside the bounds of the data).
        If set to 'extrapolate', the function will extrapolate the values.
    bounds_error : bool, optional, default=False
        If True, raises an error when attempting to interpolate outside the bounds of the data.
        If False, the `fill_value` will be used for out-of-bounds data.

    Returns:
    --------
    function
        An interpolation function that can be used to approximate y values for given x inputs.

    Notes:
    ------
    This function uses `scipy.interpolate.interp1d` to create a linear interpolation function from
    the provided x and y data.
    """
    from scipy.interpolate import interp1d
    output = interp1d(data.x, data.y, kind='linear', fill_value=fill_value, bounds_error=bounds_error)
    return output


def exp(x=1):
    """
    Compute Euler's number raised to the power of x.

    Parameters:
    -----------
    x : float, optional, default=1
        The exponent to which Euler's number (e) is raised.

    Returns:
    --------
    float
        The value of e raised to the power of x.

    Notes:
    ------
    This function uses `numpy.exp` to compute the exponential of the input value.
    """
    from numpy import exp
    output = exp(x)
    return output


## Normal Distribution ##########################

def dnorm(x, mean=0, sd=1):
    """
    Computes the probability density function (PDF) of a normal distribution.

    Parameters:
    x : array-like
        The input values where the PDF is evaluated.
    mean : float, optional
        The mean (center) of the normal distribution (default is 0).
    sd : float, optional
        The standard deviation (spread) of the normal distribution (default is 1).

    Returns:
    pandas.Series
        A Series object containing the computed PDF values.

    Example:
    >>> dnorm([0, 1, 2], mean=1, sd=1)
    0    0.241971
    1    0.398942
    2    0.241971
    dtype: float64
    """
    from scipy.stats import norm
    from pandas import Series
    output = norm.pdf(x, loc=mean, scale=sd)
    output = Series(output)
    return output

def pnorm(x, mean=0, sd=1):
    """
    Computes the cumulative distribution function (CDF) of a normal distribution.

    Parameters:
    x : array-like
        The input values where the CDF is evaluated.
    mean : float, optional
        The mean (center) of the normal distribution (default is 0).
    sd : float, optional
        The standard deviation (spread) of the normal distribution (default is 1).

    Returns:
    pandas.Series
        A Series object containing the computed CDF values.

    Example:
    >>> pnorm([0, 1, 2], mean=1, sd=1)
    0    0.158655
    1    0.500000
    2    0.841345
    dtype: float64
    """
    from scipy.stats import norm  # Import norm from scipy.stats for CDF computation
    from pandas import Series     # Import Series from pandas to return results as a Series

    output = norm.cdf(x, loc=mean, scale=sd)  # Compute the CDF for given x, mean, and sd
    output = Series(output)  # Convert the output to a pandas Series

    return output

def qnorm(x, mean=0, sd=1):
    """
    Computes the quantile function (inverse CDF) of a normal distribution.

    Parameters:
    x : array-like
        The quantiles to evaluate.
    mean : float, optional
        The mean (center) of the normal distribution (default is 0).
    sd : float, optional
        The standard deviation (spread) of the normal distribution (default is 1).

    Returns:
    float or array-like
        The computed quantiles corresponding to the input probabilities.

    Example:
    >>> qnorm([0.25, 0.5, 0.75], mean=1, sd=1)
    0   0.324918 
    1   1.
    2   1.675082
    dtype: float64
    """
    from scipy.stats import norm  # Import norm from scipy.stats for inverse CDF (PPF) computation
    from pandas import Series     # Import Series from pandas for consistent data handling

    output = norm.ppf(x, loc=mean, scale=sd)  # Compute the inverse CDF for given x, mean, and sd
    output = Series(output)  # Convert the output to a pandas Series
    return output

def rnorm(n, mean=0, sd=1):
    """
    Generates random samples from a normal distribution.

    Parameters:
    n : int
        The number of random samples to generate.
    mean : float, optional
        The mean (center) of the normal distribution (default is 0).
    sd : float, optional
        The standard deviation (spread) of the normal distribution (default is 1).

    Returns:
    pandas.Series
        A Series object containing the generated random samples.

    Example:
    >>> rnorm(5, mean=1, sd=1)
    0    1.327219
    1    0.807807
    2    1.239399
    3    1.190307
    4    0.927883
    dtype: float64
    """
    from scipy.stats import norm  # Import norm from scipy.stats for random sample generation
    from pandas import Series     # Import Series from pandas to return results as a Series

    output = norm.rvs(loc=mean, scale=sd, size=n)  # Generate n random samples with given mean and sd
    output = Series(output)  # Convert the output to a pandas Series

    return output

## Exponential Distribution ##########################
def dexp(x, rate=0.01):
    """
    Computes the probability density function (PDF) of an exponential distribution.

    Parameters:
    x : array-like
        The input values where the PDF is evaluated.
    rate : float, optional
        The rate parameter (lambda) of the exponential distribution (default is 0.01).
        Note: The scale parameter is the inverse of the rate (1/rate).

    Returns:
    pandas.Series
        A Series object containing the computed PDF values.

    Example:
    >>> dexp([1, 2, 3], rate=0.5)
    0    0.303265
    1    0.183939
    2    0.111565
    dtype: float64
    """
    from scipy.stats import expon  # Import expon from scipy.stats for PDF computation
    from pandas import Series      # Import Series from pandas to return results as a Series

    output = expon.pdf(x, loc=0, scale=1/rate)  # Compute the PDF for given x and rate
    output = Series(output)  # Convert the output to a pandas Series

    return output

def pexp(x, rate=0.01):
    """
    Computes the cumulative distribution function (CDF) of an exponential distribution.

    Parameters:
    x : array-like
        The input values where the CDF is evaluated.
    rate : float, optional
        The rate parameter (lambda) of the exponential distribution (default is 0.01).
        Note: The scale parameter is the inverse of the rate (1/rate).

    Returns:
    pandas.Series
        A Series object containing the computed CDF values.

    Example:
    >>> pexp([1, 2, 3], rate=0.5)
    0    0.393469
    1    0.632121
    2    0.776870
    dtype: float64
    """
    from scipy.stats import expon  # Import expon from scipy.stats for CDF computation
    from pandas import Series      # Import Series from pandas to return results as a Series

    output = expon.cdf(x, loc=0, scale=1/rate)  # Compute the CDF for given x and rate
    output = Series(output)  # Convert the output to a pandas Series

    return output

def qexp(x, rate=0.01):
    """
    Computes the quantile function (inverse CDF) of an exponential distribution.

    Parameters:
    x : array-like
        The quantiles to evaluate.
    rate : float, optional
        The rate parameter (lambda) of the exponential distribution (default is 0.01).
        Note: The scale parameter is the inverse of the rate (1/rate).

    Returns:
    pandas.Series
        A Series object containing the computed quantiles.

    Example:
    >>> qexp([0.25, 0.5, 0.75], rate=0.5)
    0    0.693147
    1    1.386294
    2    2.079442
    dtype: float64
    """
    from scipy.stats import expon  # Import expon from scipy.stats for inverse CDF (PPF) computation
    from pandas import Series      # Import Series from pandas to return results as a Series

    output = expon.ppf(x, loc=0, scale=1/rate)  # Compute the inverse CDF for given x and rate
    output = Series(output)  # Convert the output to a pandas Series

    return output

def rexp(n, rate=0.01):
    """
    Generates random samples from an exponential distribution.

    Parameters:
    n : int
        The number of random samples to generate.
    rate : float, optional
        The rate parameter (lambda) of the exponential distribution (default is 0.01).
        Note: The scale parameter is the inverse of the rate (1/rate).

    Returns:
    pandas.Series
        A Series object containing the generated random samples.

    Example:
    >>> rexp(5, rate=0.5)
    0    0.826784
    1    1.054297
    2    0.587229
    3    1.758107
    4    1.235874
    dtype: float64
    """
    from scipy.stats import expon  # Import expon from scipy.stats for random sample generation
    from pandas import Series      # Import Series from pandas to return results as a Series

    output = expon.rvs(loc=0, scale=1/rate, size=n)  # Generate n random samples with given rate
    output = Series(output)  # Convert the output to a pandas Series

    return output


## Weibull Distribution ##########################
def dweibull(x, shape=2, scale=1):
    """
    Computes the probability density function (PDF) of a Weibull distribution.

    Parameters:
    x : array-like
        The input values where the PDF is evaluated.
    shape : float, optional
        The shape parameter m of the Weibull distribution (default is 2).
    scale : float, optional
        The scale parameter c of the Weibull distribution (default is 1).

    Returns:
    pandas.Series
        A Series object containing the computed PDF values.

    Example:
    >>> dweibull([1, 2, 3], shape=2, scale=1)
    0    0.735759
    1    0.270671
    2    0.059897
    dtype: float64
    """
    from scipy.stats import weibull_min  # Import weibull_min from scipy.stats for PDF computation
    from pandas import Series            # Import Series from pandas to return results as a Series

    output = weibull_min.pdf(x, c=shape, scale=scale)  # Compute the PDF for given x, shape, and scale
    output = Series(output)  # Convert the output to a pandas Series

    return output

def pweibull(x, shape=2, scale=1):
    """
    Computes the cumulative distribution function (CDF) of a Weibull distribution.

    Parameters:
    x : array-like
        The input values where the CDF is evaluated.
    shape : float, optional
        The shape parameter m of the Weibull distribution (default is 2).
    scale : float, optional
        The scale parameter c of the Weibull distribution (default is 1).

    Returns:
    pandas.Series
        A Series object containing the computed CDF values.

    Example:
    >>> pweibull([1, 2, 3], shape=2, scale=1)
    0    0.632121
    1    0.981684
    2    0.999664
    dtype: float64
    """
    from scipy.stats import weibull_min  # Import weibull_min from scipy.stats for CDF computation
    from pandas import Series            # Import Series from pandas to return results as a Series

    output = weibull_min.cdf(x, c=shape, scale=scale)  # Compute the CDF for given x, shape, and scale
    output = Series(output)  # Convert the output to a pandas Series

    return output

def qweibull(x, shape=2, scale=1):
    """
    Computes the quantile function (inverse CDF) of a Weibull distribution.

    Parameters:
    x : array-like
        The quantiles to evaluate.
    shape : float, optional
        The shape parameter m of the Weibull distribution (default is 2).
    scale : float, optional
        The scale parameter c of the Weibull distribution (default is 1).

    Returns:
    pandas.Series
        A Series object containing the computed quantiles.

    Example:
    >>> qweibull([0.25, 0.5, 0.75], shape=2, scale=1)
    0    0.560573
    1    0.832555
    2    1.177410
    dtype: float64
    """
    from scipy.stats import weibull_min  # Import weibull_min from scipy.stats for inverse CDF (PPF) computation
    from pandas import Series            # Import Series from pandas to return results as a Series

    output = weibull_min.ppf(x, c=shape, scale=scale)  # Compute the inverse CDF for given x, shape, and scale
    output = Series(output)  # Convert the output to a pandas Series

    return output

def rweibull(n, shape=2, scale=1):
    """
    Generates random samples from a Weibull distribution.

    Parameters:
    n : int
        The number of random samples to generate.
    shape : float, optional
        The shape parameter m of the Weibull distribution (default is 2).
    scale : float, optional
        The scale parameter c of the Weibull distribution (default is 1).

    Returns:
    pandas.Series
        A Series object containing the generated random samples.

    Example:
    >>> rweibull(5, shape=2, scale=1)
    0    0.789138
    1    0.958812
    2    0.551638
    3    0.631681
    4    1.035347
    dtype: float64
    """
    from scipy.stats import weibull_min  # Import weibull_min from scipy.stats for random sample generation
    from pandas import Series            # Import Series from pandas to return results as a Series

    output = weibull_min.rvs(c=shape, scale=scale, size=n)  # Generate n random samples with given shape and scale
    output = Series(output)  # Convert the output to a pandas Series

    return output


## Gamma Distribution ##########################
def dgamma(x, shape=2, rate=1):
    """
    Computes the probability density function (PDF) of a Gamma distribution.

    Parameters:
    x : array-like
        The input values where the PDF is evaluated.
    shape : float, optional
        The shape parameter of the Gamma distribution (default is 2).
    rate : float, optional
        The rate parameter (inverse of scale) of the Gamma distribution (default is 1).

    Returns:
    pandas.Series
        A Series object containing the computed PDF values.

    Example:
    >>> dgamma([1, 2, 3], shape=2, rate=1)
    0    0.183940
    1    0.270671
    2    0.149361
    dtype: float64
    """
    from scipy.stats import gamma
    from pandas import Series

    output = gamma.pdf(x, a=shape, scale=1/rate)
    output = Series(output)
    return output

def pgamma(x, shape=2, rate=1):
    """
    Computes the cumulative distribution function (CDF) of a Gamma distribution.

    Parameters:
    x : array-like
        The input values where the CDF is evaluated.
    shape : float, optional
        The shape parameter of the Gamma distribution (default is 2).
    rate : float, optional
        The rate parameter (inverse of scale) of the Gamma distribution (default is 1).

    Returns:
    pandas.Series
        A Series object containing the computed CDF values.

    Example:
    >>> pgamma([1, 2, 3], shape=2, rate=1)
    0    0.264241
    1    0.593994
    2    0.800852
    dtype: float64
    """
    from scipy.stats import gamma
    from pandas import Series

    output = gamma.cdf(x, a=shape, scale=1/rate)
    output = Series(output)
    return output

def qgamma(x, shape=2, rate=1):
    """
    Compute the quantile (inverse cumulative distribution function) of the gamma distribution
    for given probabilities.

    Parameters:
    -----------
    x : array-like
        A list or array of probabilities for which the quantiles need to be calculated.
    shape : float, optional, default=2
        The shape parameter (k) of the gamma distribution.
    rate : float, optional, default=1
        The rate parameter (λ) of the gamma distribution, which is the inverse of the scale parameter.

    Returns:
    --------
    pandas.Series
        A Series object containing the calculated quantiles corresponding to the input probabilities.
    
    Notes:
    ------
    This function uses `scipy.stats.gamma.ppf` to compute the quantiles of the gamma distribution.
    The shape parameter corresponds to the 'k' parameter in the gamma distribution, and the rate is the inverse of the scale parameter.
    """
    from scipy.stats import gamma
    from pandas import Series
    output = gamma.ppf(x, a=shape, scale=1/rate)
    output = Series(output)
    return output


def rgamma(n, shape=2, rate=1):
    """
    Generate random samples from the gamma distribution.

    Parameters:
    -----------
    n : int
        The number of random samples to generate.
    shape : float, optional, default=2
        The shape parameter (k) of the gamma distribution.
    rate : float, optional, default=1
        The rate parameter (λ) of the gamma distribution, which is the inverse of the scale parameter.

    Returns:
    --------
    pandas.Series
        A Series object containing the generated random samples from the gamma distribution.
    
    Notes:
    ------
    This function uses `scipy.stats.gamma.rvs` to generate the random samples from the gamma distribution.
    The shape parameter corresponds to the 'k' parameter, and the rate is the inverse of the scale parameter.
    """
    from scipy.stats import gamma
    from pandas import Series
    output = gamma.rvs(a=shape, scale=1/rate, size=n)
    output = Series(output)
    return output

## Poisson Distribution ##########################

def dpois(x, mu=1):
    """
    Computes the probability mass function (PMF) of a Poisson distribution.

    Parameters:
    x : array-like
        The input values where the PMF is evaluated.
    mu : float, optional
        The expected number of occurrences (mean) of the Poisson distribution (default is 1).

    Returns:
    pandas.Series
        A Series object containing the computed PMF values.

    Example:
    >>> dpois([0, 1, 2], mu=1)
    0    0.367879
    1    0.367879
    2    0.183940
    dtype: float64
    """
    from scipy.stats import poisson
    from pandas import Series

    output = poisson.pmf(x, mu=mu)
    output = Series(output)
    return output

def ppois(x, mu=1):
    """
    Computes the cumulative distribution function (CDF) of a Poisson distribution.

    Parameters:
    x : array-like
        The input values where the CDF is evaluated.
    mu : float, optional
        The expected number of occurrences (mean) of the Poisson distribution (default is 1).

    Returns:
    pandas.Series
        A Series object containing the computed CDF values.

    Example:
    >>> ppois([0, 1, 2], mu=1)
    0    0.367879
    1    0.735759
    2    0.919699
    dtype: float64
    """
    from scipy.stats import poisson
    from pandas import Series

    output = poisson.cdf(x, mu=mu)
    output = Series(output)
    return output

def qpois(x, mu=1):
    """
    Computes the quantile function (inverse CDF) of a Poisson distribution.

    Parameters:
    x : array-like
        The quantiles to evaluate.
    mu : float, optional
        The expected number of occurrences (mean) of the Poisson distribution (default is 1).

    Returns:
    pandas.Series
        A Series object containing the computed quantiles.

    Example:
    >>> qpois([0.25, 0.5, 0.75], mu=1)
    0    0.0
    1    1.0
    2    2.0
    dtype: float64
    """
    from scipy.stats import poisson
    from pandas import Series

    output = poisson.ppf(x, mu=mu)
    output = Series(output)
    return output

def rpois(n, mu=1):
    """
    Generates random samples from a Poisson distribution.

    Parameters:
    n : int
        The number of random samples to generate.
    mu : float, optional
        The expected number of occurrences (mean) of the Poisson distribution (default is 1).

    Returns:
    pandas.Series
        A Series object containing the generated random samples.

    Example:
    >>> rpois(5, mu=1)
    0    0
    1    1
    2    2
    3    0
    4    1
    dtype: int64
    """
    from scipy.stats import poisson
    from pandas import Series

    output = poisson.rvs(mu=mu, size=n)
    output = Series(output)
    return output

## Binomial Distribution ##########################

def dbinom(x, size=1, prob=0.5):
    """
    Computes the probability mass function (PMF) of a Binomial distribution.

    Parameters:
    x : array-like
        The input values where the PMF is evaluated.
    size : int, optional
        The number of trials (default is 1).
    prob : float, optional
        The probability of success on each trial (default is 0.5).

    Returns:
    pandas.Series
        A Series object containing the computed PMF values.

    Example:
    >>> dbinom([0, 1, 2], size=2, prob=0.5)
    0    0.250
    1    0.500
    2    0.250
    dtype: float64
    """
    from scipy.stats import binom
    from pandas import Series

    output = binom.pmf(x, n=size, p=prob)
    output = Series(output)
    return output

def pbinom(x, size=1, prob=0.5):
    """
    Computes the cumulative distribution function (CDF) of a Binomial distribution.

    Parameters:
    x : array-like
        The input values where the CDF is evaluated.
    size : int, optional
        The number of trials (default is 1).
    prob : float, optional
        The probability of success on each trial (default is 0.5).

    Returns:
    pandas.Series
        A Series object containing the computed CDF values.

    Example:
    >>> pbinom([0, 1, 2], size=2, prob=0.5)
    0    0.250
    1    0.750
    2    1.000
    dtype: float64
    """
    from scipy.stats import binom
    from pandas import Series

    output = binom.cdf(x, n=size, p=prob)
    output = Series(output)
    return output

def qbinom(x, size=1, prob=0.5):
    """
    Computes the quantile function (inverse CDF) of a Binomial distribution.

    Parameters:
    x : array-like
        The quantiles to evaluate.
    size : int, optional
        The number of trials (default is 1).
    prob : float, optional
        The probability of success on each trial (default is 0.5).

    Returns:
    pandas.Series
        A Series object containing the computed quantiles.

    Example:
    >>> qbinom([0.25, 0.5, 0.75], size=2, prob=0.5)
    0    0.0
    1    1.0
    2    2.0
    dtype: float64
    """
    from scipy.stats import binom
    from pandas import Series

    output = binom.ppf(x, n=size, p=prob)
    output = Series(output)
    return output

def rbinom(n, size=1, prob=0.5):
    """
    Generates random samples from a Binomial distribution.

    Parameters:
    n : int
        The number of random samples to generate.
    size : int, optional
        The number of trials (default is 1).
    prob : float, optional
        The probability of success on each trial (default is 0.5).

    Returns:
    pandas.Series
        A Series object containing the generated random samples.

    Example:
    >>> rbinom(5, size=2, prob=0.5)
    0    1
    1    2
    2    1
    3    0
    4    1
    dtype: int64
    """
    from scipy.stats import binom
    from pandas import Series

    output = binom.rvs(n=size, p=prob, size=n)
    output = Series(output)
    return output

## Uniform Distribution ##########################

def dunif(x, min=0, max=1):
    """
    Computes the probability density function (PDF) of a Uniform distribution.

    Parameters:
    x : array-like
        The input values where the PDF is evaluated.
    min : float, optional
        The lower bound of the Uniform distribution (default is 0).
    max : float, optional
        The upper bound of the Uniform distribution (default is 1).

    Returns:
    pandas.Series
        A Series object containing the computed PDF values.

    Example:
    >>> dunif([0.1, 0.5, 0.9], min=0, max=1)
    0    1.0
    1    1.0
    2    1.0
    dtype: float64
    """
    from scipy.stats import uniform
    from pandas import Series

    output = uniform.pdf(x, loc=min, scale=max-min)
    output = Series(output)
    return output

def punif(x, min=0, max=1):
    """
    Computes the cumulative distribution function (CDF) of a Uniform distribution.

    Parameters:
    x : array-like
        The input values where the CDF is evaluated.
    min : float, optional
        The lower bound of the Uniform distribution (default is 0).
    max : float, optional
        The upper bound of the Uniform distribution (default is 1).

    Returns:
    pandas.Series
        A Series object containing the computed CDF values.

    Example:
    >>> punif([0.1, 0.5, 0.9], min=0, max=1)
    0    0.1
    1    0.5
    2    0.9
    dtype: float64
    """
    from scipy.stats import uniform
    from pandas import Series

    output = uniform.cdf(x, loc=min, scale=max-min)
    output = Series(output)
    return output
def qunif(x, min=0, max=1):
    """
    Compute the quantile (inverse cumulative distribution function) of the uniform distribution
    for given probabilities.

    Parameters:
    -----------
    x : array-like
        A list or array of probabilities for which the quantiles need to be calculated.
    min : float, optional, default=0
        The lower bound of the uniform distribution.
    max : float, optional, default=1
        The upper bound of the uniform distribution.

    Returns:
    --------
    pandas.Series
        A Series object containing the calculated quantiles corresponding to the input probabilities.
    
    Notes:
    ------
    This function uses `scipy.stats.uniform.ppf` to compute the quantiles.
    """
    from scipy.stats import uniform
    from pandas import Series
    output = uniform.ppf(x, loc=min, scale=max)
    output = Series(output)
    return output


def runif(n, min=0, max=1):
    """
    Generate random samples from a uniform distribution.

    Parameters:
    -----------
    n : int
        The number of random samples to generate.
    min : float, optional, default=0
        The lower bound of the uniform distribution.
    max : float, optional, default=1
        The upper bound of the uniform distribution.

    Returns:
    --------
    pandas.Series
        A Series object containing the generated random samples from the uniform distribution.
    
    Notes:
    ------
    This function uses `scipy.stats.uniform.rvs` to generate the random samples.
    """
    from scipy.stats import uniform
    from pandas import Series
    output = uniform.rvs(loc=min, scale=max, size=n)
    output = Series(output)
    return output
