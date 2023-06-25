from random import gauss, uniform, normalvariate
from datetime import timedelta
import numpy as np

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def generate_stock_prices_gaussian(start_date, end_date):
    price = uniform(1,100)
    prices = {}
    for single_date in daterange(start_date, end_date):
        daily_return = gauss(0.0005, 0.02)  # mean and standard deviation
        price *= (1 + daily_return)
        prices[single_date] = round(price, 2)
    return prices

def generate_stock_prices_gbm(start_date, end_date):
    S0 = uniform(1,100)  # initial stock price
    mu = 0.0005  # drift
    sigma = 0.02  # volatility
    T = (end_date - start_date).days / 365.0  # time period in years
    N = (end_date - start_date).days  # number of increments

    # Generate a Brownian motion
    dt = T / N
    W = np.cumsum(np.sqrt(dt) * np.random.standard_normal(N))

    prices = {}
    for i, single_date in enumerate(daterange(start_date, end_date)):
        S = S0 * np.exp((mu - 0.5 * sigma**2) * (i * dt) + sigma * W[i])
        prices[single_date] = round(S, 2)
    return prices