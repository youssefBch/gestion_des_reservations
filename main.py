import streamlit as st
import pandas as pd
import numpy as np

conn = st.connection("mydatabase", type="sql")

quer = conn.query("SELECT* FROM mytable")

st.write(quer)
st.write("hello worl")

