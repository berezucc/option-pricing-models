import psycopg2
import streamlit as st

# Function to insert data into PostgreSQL (Supabase) table
@st.cache_data(ttl=600)
def insert_input_into_db(table_name, _params):
    connection = psycopg2.connect(
        host=st.secrets["connections"]["supabase"]["host"],
        user=st.secrets["connections"]["supabase"]["user"],
        password=st.secrets["connections"]["supabase"]["password"],
        database=st.secrets["connections"]["supabase"]["database"],
        port=st.secrets["connections"]["supabase"]["port"]
    )
    cursor = connection.cursor()

    columns = ', '.join(_params.keys())
    placeholders = ', '.join(['%s'] * len(_params))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    cursor.execute(query, tuple(_params.values()))
    connection.commit()

    cursor.close()
    connection.close()

# Function to query specific table
@st.cache_data(ttl=600)
def query_table(table_name):
    connection = psycopg2.connect(
        host=st.secrets["connections"]["supabase"]["host"],
        user=st.secrets["connections"]["supabase"]["user"],
        password=st.secrets["connections"]["supabase"]["password"],
        database=st.secrets["connections"]["supabase"]["database"],
        port=st.secrets["connections"]["supabase"]["port"]
    )
    cursor = connection.cursor()

    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    
    result = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    cursor.close()
    connection.close()
    
    return [dict(zip(columns, row)) for row in result]