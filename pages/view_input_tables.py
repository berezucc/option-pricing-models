import streamlit as st
import pandas as pd
from db.db import query_table

# ---------------------------------
# Tab config
# ---------------------------------
st.set_page_config(
    page_icon="📈",
    page_title="View Input Tables",
    initial_sidebar_state="expanded",
    layout="wide")

# Title
st.title("View Input Tables")

# Options for table selection
table_options = ["BlackScholesInputs", "BinomialInputs", "MonteCarloInputs"]
table_choice = st.selectbox("Choose table to view:", table_options)

# Display Table Contents
df = query_table(table_choice)
st.write(f"Table: {table_choice}")
st.dataframe(df)
