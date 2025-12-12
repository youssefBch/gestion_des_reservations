import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import text
from connectionDB import *
st.set_page_config(page_title = "Welcome To our reservation web site")
st.title("This is the Home Page.")
st.sidebar.success("Select Any Page from here")
