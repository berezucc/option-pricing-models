import numpy as np

# https://www.investopedia.com/terms/b/binomialoptionpricing.asp
class Binomial:
    def __init__(self, S, K, T, r, sigma, N):
        """
        Initialize the Binomial Option Pricing Model parameters.

        Parameters:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity (in years)
        r (float): Risk-free interest rate
        sigma (float): Volatility of the stock
        N (int): Number of time steps
        """
        self.curr_price = S
        self.strike_price = K
        self.time_to_maturity = T
        self.riskfree_interest_rate = r
        self.volatility = sigma
        self.steps = N

    def binomial_american_option(self, option_type='call'):
        """
        Calculate the Binomial option price for American options.

        Parameters:
        option_type (str): 'call' or 'put'

        Returns:
        float: The American option price
        """
        S = self.curr_price
        K = self.strike_price
        T = self.time_to_maturity
        r = self.riskfree_interest_rate
        sigma = self.volatility
        N = self.steps

        dt = T / N
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u
        p = (np.exp(r * dt) - d) / (u - d)
        discount = np.exp(-r * dt)
        
        # Initialize asset prices at maturity
        asset_prices = S * d**np.arange(N, -1, -1) * u**np.arange(0, N + 1, 1)
        
        # Initialize option values at maturity
        if option_type == 'call':
            option_values = np.maximum(0, asset_prices - K)
        else:
            option_values = np.maximum(0, K - asset_prices)
        
        # Step back through the tree
        for i in range(N - 1, -1, -1):
            asset_prices = S * d**np.arange(i, -1, -1) * u**np.arange(0, i + 1, 1)
            option_values = discount * (p * option_values[1:i + 2] + (1 - p) * option_values[0:i + 1])
            if option_type == 'call':
                option_values = np.maximum(option_values, asset_prices - K)
            else:
                option_values = np.maximum(option_values, K - asset_prices)
        
        return option_values[0]

# # Example usage
# S = 100  # Current stock price
# K = 100  # Strike price
# T = 1    # Time to maturity (in years)
# r = 0.05  # Risk-free interest rate
# sigma = 0.2  # Volatility
# N = 50  # Number of time steps

# # Instantiate the BinomialOption class
# binomial_option = Binomial(S, K, T, r, sigma, N)

# # Calculate and print the price of the American call option
# call_option_price = binomial_option.binomial_american_option(option_type='call')
# print("Binomial American Call Option Price:", call_option_price)

# # Calculate and print the price of the American put option
# put_option_price = binomial_option.binomial_american_option(option_type='put')
# print("Binomial American Put Option Price:", put_option_price)
