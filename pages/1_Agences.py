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


def map():
    logiLatitTable = conn.query("SELECT longi,lati FROM VILLE")
    df = pd.DataFrame(logiLatitTable)
    st.write(df)
    col1,col2,col3 = st.columns(3)

    # Center map on the average location
    avg_lat = df['lati'].mean()
    avg_long = df['longi'].mean()
    m = folium.Map(location=[avg_lat, avg_long], zoom_start=6)
    # Add markers for each city
    for index,row in df.iterrows():
        folium.Marker(
            [row["lati"],row["longi"]],
            popup="Liberty Bell",
            tooltip="Liberty Bell"
        ).add_to(m)

    # call to render Folium map in Streamlit
    st_data = st_folium(m, width=725)

map()