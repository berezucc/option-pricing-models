import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from models.american.Binomial import Binomial
from models.european.BlackScholes import BlackScholes
from matplot.plotting import call_payoff, put_payoff, plot_payoff

# ---------------------------------
# Tab config
# ---------------------------------
st.set_page_config(
    page_icon="📈",
    page_title="Option Pricing Models - Nikita Berezyuk",
    initial_sidebar_state="expanded",
    layout="wide")


# ---------------------------------
# Sidebar
# ---------------------------------
with st.sidebar:
    st.title("📈 Option Pricing Models")
    linkedin_url = "https://www.linkedin.com/in/nikita-berezyuk/"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25">`Nikita Berezyuk`</a>', unsafe_allow_html=True)
    
    model = st.radio(
        "Choose an options pricing model",
        ("American (Black-Scholes)", "European (Binomial)")
    )

    S = st.number_input("Current Asset Price", value=100.0, step=1.0)
    K = st.number_input("Strike Price", value=100.0, step=1.0)
    T = st.number_input("Time to Maturity (in years)", value=1.0)
    r = st.number_input("Risk-free Interest Rate", value=0.05)
    sigma = st.number_input("Volatility", value=0.2)

    if "European" in model:
        N = st.number_input("Number of Time Steps", value=50.0, step=1.0)


# ---------------------------------
# Option Pricing Section Calculation
# ---------------------------------
st.divider()

if "Black-Scholes" in model:
    bs = BlackScholes(S, K, T, r, sigma)
    call_price, put_price = bs.call_price(), bs.put_price()
elif "Binomial" in model:
    binomial_option = Binomial(S, K, T, r, sigma, N)
    call_price, put_price = binomial_option.binomial_american_option(option_type='call'), binomial_option.binomial_american_option(option_type='put')

# Display Call and Put Prices
call_price_col, put_price_col = st.columns([1,1], gap="small")

# Custom styles for metrics
st.markdown("""
    <style>
    .metric-container {
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        text-align: center;
    }
    .metric-call {
        background-color: #d4edda;
        color: #155724;
    }
    .metric-put {
        background-color: #f8d7da;
        color: #721c24;
    }
    .metric-label {
        font-size: 1.5em;
        font-weight: bold;
    }
    .metric-value {
        font-size: 2.0em;
    }
    </style>
""", unsafe_allow_html=True)

with call_price_col:
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">Call Value</div>
                <div class="metric-value">${call_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with put_price_col:
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">Put Value</div>
                <div class="metric-value">${put_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ---------------------------------
# Heatmap Section
# ---------------------------------
st.divider()

call_col, put_col = st.columns(2)

# Call heatmap
with call_col:
    st.header("Call Price Heatmap")

# Put heatmap
with put_col:
    st.header("Put Price Heatmap")


# ---------------------------------
# Payoff Diagrams
# ---------------------------------
st.divider()

# Stock price range
stock_prices = np.arange(0.75 * S, 1.45 * S, 1)

# Calculate the payoff for the long call & put options
payoff_long_call = call_payoff(stock_prices, K, call_price)
payoff_long_put = put_payoff(stock_prices, K, put_price)

payoff_long_call_col, payoff_long_put_col = st.columns(2)

with payoff_long_call_col:
    st.header("Long Call P&L")
    fig_call = plot_payoff(stock_prices, payoff_long_call, 'Call', 'g')
    st.pyplot(fig_call)

with payoff_long_put_col:
    st.header("Long Put P&L")
    fig_put = plot_payoff(stock_prices, payoff_long_put, 'Put', 'r')
    st.pyplot(fig_put)
