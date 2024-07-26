"""
import mysql.connector
import streamlit as st

# Function to insert data into MySQL table
@st.cache_data(ttl=600)
def insert_input_into_db(table_name, _params):
    connection = mysql.connector.connect(
        host=st.secrets["connections"]["mysql"]["host"],
        user=st.secrets["connections"]["mysql"]["username"],
        password=st.secrets["connections"]["mysql"]["password"],
        database=st.secrets["connections"]["mysql"]["database"],
        port=st.secrets["connections"]["mysql"]["port"]
    )
    cursor = connection.cursor()

    columns = ', '.join(_params.keys())
    placeholders = ', '.join(['%s'] * len(_params))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    cursor.execute(query, tuple(_params.values()))
    connection.commit()

    cursor.close()
    connection.close()

# Function to query specifc table
@st.cache_data(ttl=600)
def query_table(table_name):
    connection = mysql.connector.connect(
        host=st.secrets["connections"]["mysql"]["host"],
        user=st.secrets["connections"]["mysql"]["username"],
        password=st.secrets["connections"]["mysql"]["password"],
        database=st.secrets["connections"]["mysql"]["database"],
        port=st.secrets["connections"]["mysql"]["port"]
    )
    cursor = connection.cursor()
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()
"""