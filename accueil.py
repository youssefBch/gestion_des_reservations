import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import text
import folium
from streamlit_folium import st_folium
from connectionDB import *
st.set_page_config(page_title = "Welcome To our reservation web site")
st.title("This is the Home Page.")
st.sidebar.success("Select Any Page from here")



logiLatitTable = conn.query("SELECT longi,lati FROM VILLE")
df = pd.DataFrame(logiLatitTable)
st.write(df)
col1,col2,col3 = st.columns(3)
for index,row in df.iterrows():
    m = folium.Map(location=[row["lati"],row["longi"]], zoom_start=16)
    folium.Marker([row["lati"],row["longi"]], popup="Liberty Bell", tooltip="Liberty Bell").add_to(m)

     # call to render Folium map in Streamlit
    st_data = st_folium(m, width=725)
    st_data