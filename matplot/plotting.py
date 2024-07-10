import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def call_payoff(stock_prices, strike_price, premium):
    # If stock price > strike price, the payoff is stock price - strike price - premium
    # Else it's -premium
    return np.where(stock_prices > strike_price, stock_prices - strike_price, 0) - premium

def put_payoff(stock_prices, strike_price, premium):
    # If stock price < strike price, the payoff is strike price - stock price - premium
    # Else it's -premium
    return np.where(stock_prices < strike_price, strike_price - stock_prices, 0) - premium

def plot_payoff(stock_prices, payoff, option_type, color):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(stock_prices, payoff, label=f'Long {option_type}', color=color)
    max_y = max(abs(payoff.min()), abs(payoff.max()))
    ax.set_ylim(-max_y, max_y)  # Set y-axis limits as equal in both directions
    plt.xlabel('Stock Price')
    plt.ylabel('P&L')
    plt.legend()
    plt.title(f'Long {option_type} Option Payoff Diagram')
    return fig
