import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import text
def headerEdit():
    st.logo("assets/ensak.png",size="medium")
    st.set_page_config(page_title="Hotel Manager", layout="wide", page_icon="🏨")
    st.html("""
    <style>
        .stSidebar {
            position: relative;
            width: 280px;            
        }
        .st-emotion-cache-13k62yr {
            inset: 5px;
        }
        .st-emotion-cache-1wxyy64 {
        height: 2.5rem;
    
        }
    </style>
    """)

