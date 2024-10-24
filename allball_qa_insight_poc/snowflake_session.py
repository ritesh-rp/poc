import streamlit as st

# Initialize connection.
def create_snowflake_session():
    return st.connection("snowflake").session()
