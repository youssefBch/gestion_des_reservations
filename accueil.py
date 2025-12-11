import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import text
conn = st.connection("mydatabase", type="sql")