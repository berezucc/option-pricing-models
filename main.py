import streamlit as st
import pandas as pd
import numpy as np

from db.db import insert_input_into_db

from models.american.Binomial import BinomialAmericanOption
from models.european.BlackScholes import BlackScholes
from models.european.MonteCarlo import MonteCarlo

from matplot.payoff_plotting import long_call_payoff, long_put_payoff, short_call_payoff, short_put_payoff, plot_payoff
from matplot.heatmap_plotting import heatmap_plot

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

    # Option pricing model inputs
    model = st.radio(
        "Choose an options pricing model",
        ("Black-Scholes (American)", "Binomial Option (European)", "Monte-Carlo Simulation (European)")
    )

    S = st.number_input("Current Asset Price", value=100.0, step=1.0)
    K = st.number_input("Strike Price", value=100.0, step=1.0)
    T = st.number_input("Time to Expiry (in years)", value=1.0)
    r = st.number_input("Risk-free Interest Rate", value=0.05)
    sigma = st.number_input("Volatility", value=0.2)

    if "Binomial Option" in model:
        N = st.number_input("Number of Time Steps", value=50.0, step=1.0)
    elif "Monte-Carlo" in model:
        N = st.number_input("Number of Simulation Steps", value=10000.0, step=1000.0)
    
    calculate = st.button("Calculate")

    st.divider()


# ---------------------------------
# Main Content
# ---------------------------------
if calculate:
    # Insert input parameters into the models table
    if "Black-Scholes" in model:
        table_name = "BlackScholesInputs"
        params = {
            "StockPrice": S,
            "StrikePrice": K,
            "InterestRate": r,
            "Volatility": sigma,
            "TimeToExpiry": T
        }
    elif "Binomial" in model:
        table_name = "BinomialInputs"
        params = {
            "StockPrice": S,
            "StrikePrice": K,
            "InterestRate": r,
            "Volatility": sigma,
            "TimeToExpiry": T,
            "Steps": N
        }
    elif "Monte-Carlo" in model:
        table_name = "MonteCarloInputs"
        params = {
            "StockPrice": S,
            "StrikePrice": K,
            "InterestRate": r,
            "Volatility": sigma,
            "TimeToExpiry": T,
            "Simulations": N
        }
    insert_input_into_db(table_name, params)

    # ---------------------------------
    # Display option calculation inputs
    # ---------------------------------
    # regex to filter out model name and option type
    model_name = model.split('(')[0].strip()
    option_type = "European" if "European" in model else "American"
    option_meaning = ("European options can only be exercised at expiration. The majority of CME Group options on futures are European style and can be exercised only at expiration."
                    if option_type == "European" else 
                    "American options can be exercised at any time before expiration. Some of the notable exceptions that have American style expiration are the quarterly options on the S&P500 futures contracts, SOFR options, and Treasury options.")

    st.title(f"{model_name} Pricing Model")

    # Table of Inputs
    input_data = {
        "Current Asset Price": [S],
        "Strike Price": [K],
        "Time to Expiry (Years)": [T],
        "Volatility (σ)": [sigma],
        "Risk-Free Interest Rate": [r],
    }
    if "European" in model:
        input_data["Number of Time Steps"] = [N]
    input_df = pd.DataFrame(input_data)
    st.table(input_df)

    # Display the model name, type and meaning 
    st.markdown(f"""
        <div style="
            padding: 20px;
            border-radius: 5px;
            background-color: #223344;
            color: #ffffff;
            border: 1px solid #34495e;
            margin-bottom: 20px;
        ">
            <h4 style="margin: 0;">{option_type} Option Model</h4>
            <p style="margin: 0;">{option_type}: {option_meaning}</p>
        </div>
    """, unsafe_allow_html=True)

    # ---------------------------------
    # Option Pricing Section Calculation
    # ---------------------------------
    st.divider()

    if "Black-Scholes" in model:
        bs = BlackScholes(S, K, T, r, sigma)
        call_price, put_price = bs.call_price(), bs.put_price()
    elif "Binomial" in model:
        binomial = BinomialAmericanOption(S, K, T, r, sigma, N)
        call_price, put_price = binomial.call_price(), binomial.put_price()
    elif "Monte-Carlo" in model:
        montecarlo = MonteCarlo(S, K, T, r, sigma, N)
        call_price, put_price = montecarlo.call_price(), montecarlo.put_price()

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

    # Create grids of spot prices and volatilities
    spot_prices = np.arange(0.75 * S, 1.25 * S, 5)  # Min spot price to max spot price
    volatilities = np.linspace(0.01, 0.99, 10)  # Min volatility to max volatility

    # Initialize matrices to hold call and put prices
    call_prices = np.zeros((len(volatilities), len(spot_prices)))
    put_prices = np.zeros((len(volatilities), len(spot_prices)))

    # Calculate call and put prices for each combination of spot price and volatility
    for i, sigma in enumerate(volatilities):
        for j, S in enumerate(spot_prices):
            bs = BlackScholes(S, K, T, r, sigma)
            call_prices[i, j] = bs.call_price()
            put_prices[i, j] = bs.put_price()

    call_col, put_col = st.columns(2)

    # Call heatmap
    with call_col:
        st.header("Call Price Heatmap")
        call_heatmap = heatmap_plot(call_prices, spot_prices, volatilities, "Call")
        st.pyplot(call_heatmap)

    # Put heatmap
    with put_col:
        st.header("Put Price Heatmap")
        call_heatmap = heatmap_plot(put_prices, spot_prices, volatilities, "Put")
        st.pyplot(call_heatmap)


    # ---------------------------------
    # Payoff Diagrams
    # ---------------------------------
    st.divider()

    # Stock price range
    stock_prices = np.arange(0.75 * S, 1.45 * S, 1)

    # Calculate the payoff for the long call & put options
    payoff_long_call = long_call_payoff(stock_prices, K, call_price)
    payoff_long_put = long_put_payoff(stock_prices, K, put_price)

    payoff_long_call_col, payoff_long_put_col = st.columns(2)

    with payoff_long_call_col:
        st.header("Long Call P&L")
        fig_call = plot_payoff(stock_prices, payoff_long_call, 'Long', 'Call', 'g')
        st.pyplot(fig_call)

    with payoff_long_put_col:
        st.header("Long Put P&L")
        fig_put = plot_payoff(stock_prices, payoff_long_put, 'Long', 'Put', 'r')
        st.pyplot(fig_put)

    # Calculate the payoff for the short call & put options
    payoff_short_call = short_call_payoff(stock_prices, K, call_price)
    payoff_short_put = short_put_payoff(stock_prices, K, put_price)

    payoff_short_call_col, payoff_short_put_col = st.columns(2)

    with payoff_short_call_col:
        st.header("Short Call P&L")
        fig_call = plot_payoff(stock_prices, payoff_short_call, 'Short', 'Call', 'orange')
        st.pyplot(fig_call)

    with payoff_short_put_col:
        st.header("Short Put P&L")
        fig_put = plot_payoff(stock_prices, payoff_short_put, 'Short', 'Put', 'blue')
        st.pyplot(fig_put)
