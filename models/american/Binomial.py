import numpy as np

# https://www.investopedia.com/terms/b/binomialoptionpricing.asp
class BinomialAmericanOption:
    def __init__(self, S, K, T, r, sigma, N):
        """
        Initialize the Binomial Option pricing model parameters.

        Parameters:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity (in years)
        r (float): Risk-free interest rate
        sigma (float): Volatility of the stock
        N (int): Number of steps in the binomial tree
        """
        self.curr_price = S
        self.strike_price = K
        self.time_to_maturity = T
        self.riskfree_interest_rate = r
        self.volatility = sigma
        self.steps = N

    def _initialize_parameters(self):
        """
        Initialize parameters for the Binomial Option pricing model.

        Returns:
        tuple: Contains initialized parameters needed for the model.
        """
        S = self.curr_price
        K = self.strike_price
        T = self.time_to_maturity
        r = self.riskfree_interest_rate
        sigma = self.volatility
        N = int(self.steps)

        dt = T / N
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u
        p = (np.exp(r * dt) - d) / (u - d)
        discount = np.exp(-r * dt)
        
        return S, K, T, r, sigma, N, dt, u, d, p, discount

    def calculate_option_value(self, option_values, asset_prices, p, discount, N, K, option_type):
        """
        Calculate the option value by stepping back through the binomial tree.

        Parameters:
        option_values (np.ndarray): Initial option values at maturity
        asset_prices (np.ndarray): Asset prices at maturity
        p (float): Risk-neutral probability
        discount (float): Discount factor
        N (int): Number of steps in the binomial tree
        K (float): Strike price
        option_type (str): 'call' or 'put'

        Returns:
        float: The calculated option price
        """
        for i in range(N - 1, -1, -1):
            asset_prices = self.curr_price * (1 / np.exp(self.volatility * np.sqrt(self.time_to_maturity / self.steps)))**np.arange(i, -1, -1) * np.exp(self.volatility * np.sqrt(self.time_to_maturity / self.steps))**np.arange(0, i + 1, 1)
            option_values = discount * (p * option_values[1:i + 2] + (1 - p) * option_values[0:i + 1])
            if option_type == 'call':
                option_values = np.maximum(option_values, asset_prices - K)
            else:
                option_values = np.maximum(option_values, K - asset_prices)
        return option_values[0]

    def call_price(self):
        """
        Calculate the American call option price using the binomial model.

        Returns:
        float: The American call option price
        """
        S, K, T, r, sigma, N, dt, u, d, p, discount = self._initialize_parameters()
        asset_prices = S * d**np.arange(N, -1, -1) * u**np.arange(0, N + 1, 1)
        option_values = np.maximum(0, asset_prices - K)
        return self.calculate_option_value(option_values, asset_prices, p, discount, N, K, 'call')

    def put_price(self):
        """
        Calculate the American put option price using the binomial model.

        Returns:
        float: The American put option price
        """
        S, K, T, r, sigma, N, dt, u, d, p, discount = self._initialize_parameters()
        asset_prices = S * d**np.arange(N, -1, -1) * u**np.arange(0, N + 1, 1)
        option_values = np.maximum(0, K - asset_prices)
        return self.calculate_option_value(option_values, asset_prices, p, discount, N, K, 'put')
