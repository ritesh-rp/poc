import streamlit as st 
cnx = st.connection("snowflake")

from .player_script import *