import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def long_call_payoff(stock_prices, strike_price, premium):
    # If stock price > strike price, the payoff is stock price - strike price - premium
    # Else it's -premium
    return np.where(stock_prices > strike_price, stock_prices - strike_price, 0) - premium

def short_call_payoff(stock_prices, strike_price, premium):
    # If stock price < strike price, the payoff is +premium
    # Else it's strike price - stock price + premium
    return np.where(stock_prices < strike_price, 0, strike_price - stock_prices) + premium

def long_put_payoff(stock_prices, strike_price, premium):
    # If stock price < strike price, the payoff is strike price - stock price - premium
    # Else it's -premium
    return np.where(stock_prices < strike_price, strike_price - stock_prices, 0) - premium

def short_put_payoff(stock_prices, strike_price, premium):
    # If stock price > strike price, the payoff is +premium
    # Else it's stock price - strike price + premium
    return np.where(stock_prices > strike_price, 0, stock_prices - strike_price) + premium

def plot_payoff(stock_prices, payoff, position, option_type, color):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(stock_prices, payoff, label=f'{position} {option_type}', color=color)
    max_y = max(abs(payoff.min()), abs(payoff.max()))
    ax.set_ylim(-max_y, max_y)  # Set y-axis limits as equal in both directions
    plt.xlabel('Stock Price')
    plt.ylabel('P&L')
    plt.legend()
    plt.title(f'{position} {option_type} Option Payoff Diagram')
    return fig
