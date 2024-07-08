import numpy as np
from scipy.stats import norm

class BlackScholes():
    def __init__(self, S, K, t, r, sigma):
        self.curr_price = S
        self.strike_price = K
        self.time_to_maturity = t
        self.riskfree_interest_rate = r
        self.volatility = sigma

    def call_price(self, ):
        pass
    def put_price(self, ):
        pass