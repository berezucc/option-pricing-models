import numpy as np
from scipy.stats import norm

# https://www.investopedia.com/terms/b/blackscholes.asp
class BlackScholes:
    def __init__(self, S, K, T, r, sigma):
        """
        Initialize the Black-Scholes model parameters.

        Parameters:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity (in years)
        r (float): Risk-free interest rate
        sigma (float): Volatility of the stock
        """
        self.curr_price = S
        self.strike_price = K
        self.time_to_maturity = T
        self.riskfree_interest_rate = r
        self.volatility = sigma

    def d1(self):
        """
        Calculate d1 used in the Black-Scholes formula.

        Returns:
        float: The d1 value
        """
        return (np.log(self.curr_price / self.strike_price) + 
                (self.riskfree_interest_rate + 0.5 * self.volatility**2) * self.time_to_maturity) / (self.volatility * np.sqrt(self.time_to_maturity))
    
    def d2(self):
        """
        Calculate d2 used in the Black-Scholes formula.

        Returns:
        float: The d2 value
        """
        return self.d1() - self.volatility * np.sqrt(self.time_to_maturity)
    
    def call_price(self):
        """
        Calculate the Black-Scholes price for a European call option.

        Returns:
        float: The call option price
        """
        d1 = self.d1()
        d2 = self.d2()
        call_price = (self.curr_price * norm.cdf(d1) - 
                      self.strike_price * np.exp(-self.riskfree_interest_rate * self.time_to_maturity) * norm.cdf(d2))
        return call_price

    def put_price(self):
        """
        Calculate the Black-Scholes price for a European put option.

        Returns:
        float: The put option price
        """
        d1 = self.d1()
        d2 = self.d2()
        put_price = (self.strike_price * np.exp(-self.riskfree_interest_rate * self.time_to_maturity) * norm.cdf(-d2) - 
                     self.curr_price * norm.cdf(-d1))
        return put_price
