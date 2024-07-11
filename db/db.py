import psycopg2
import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection

# Initialize the Supabase client
@st.cache_data(ttl=600)
def init_supabase_client() -> Client:
    url = st.secrets["connections"]["supabase"]["SUPABASE_URL"]
    key = st.secrets["connections"]["supabase"]["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase_client()

# Function to insert data into Supabase table
def insert_input_into_db(table_name, _params):
    data = supabase.table(table_name).insert(_params).execute()
    return data

# Function to query specific table
def query_table(table_name):
    data = supabase.table(table_name).select("*").execute()
    df = pd.DataFrame(data.data)
    return df