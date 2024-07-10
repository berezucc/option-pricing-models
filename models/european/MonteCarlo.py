import numpy as np

# https://www.investopedia.com/articles/investing/112514/monte-carlo-simulation-basics.asp#:~:text=Monte%20Carlo%20is%20used%20for,to%20get%20the%20option%20price.
# https://corporatefinanceinstitute.com/resources/derivatives/option-pricing-models/#:~:text=Option%20Pricing%20Models%20are%20mathematical,fair%20value%20of%20an%20option.
class MonteCarlo:
    def __init__(self, S, K, T, r, sigma, N):
        """
        Initialize the MonteCarlo model parameters.

        Parameters:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity (in years)
        r (float): Risk-free interest rate
        sigma (float): Volatility of the stock
        N (int): Number of steps in the continuous time simulation
        """
        self.curr_price = S
        self.strike_price = K
        self.time_to_maturity = T
        self.riskfree_interest_rate = r
        self.volatility = sigma
        self.simulations = int(N)

    def stock_price_at_maturity(self):
        # Simulate end-of-period stock prices
        Z = np.random.standard_normal(self.simulations)
        # geometric Brownian motion model
        ST = self.curr_price * np.exp((self.riskfree_interest_rate - 0.5 * self.volatility**2) * self.time_to_maturity + self.volatility * np.sqrt(self.time_to_maturity) * Z)
        return ST

    def call_price(self):
        """
        Calculate the European call option price using the MonteCarlo model.

        Returns:
        float: The European call option price
        """
        ST = self.stock_price_at_maturity()
        payoff = np.maximum(ST - self.strike_price, 0)

        # Discount payoffs back to present value
        discount_factor = np.exp(-self.riskfree_interest_rate * self.time_to_maturity)
        option_price = discount_factor * np.mean(payoff)
        return option_price
    
    def put_price(self):
        """
        Calculate the European put option price using the MonteCarlo model.

        Returns:
        float: The European put option price
        """
        ST = self.stock_price_at_maturity()
        payoff = np.maximum(self.strike_price - ST, 0)

        # Discount payoffs back to present value
        discount_factor = np.exp(-self.riskfree_interest_rate * self.time_to_maturity)
        option_price = discount_factor * np.mean(payoff)
        return option_price
