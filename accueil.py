import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import text
import folium
from streamlit_folium import st_folium
from connectionDB import *
from headEdite import *
headerEdit()
import base64

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


st.set_page_config(page_title = "Welcome To our reservation web site")
st.title("This is the Home Page.")
st.sidebar.success("Select Any Page from here")
def profilCard(ftname,lname,imageUrl,role):
    st.html("""
    <style>
    .our-team {
          padding: 30px 0 40px;
          margin-bottom: 30px;
          background-color: #f7f5ec;
          text-align: center;
          border-radius: 10px;
          overflow: hidden;
          position: relative;
        }
        
        .our-team .picture {
          display: inline-block;
          height: 130px;
          width: 130px;
          margin-bottom: 50px;
          z-index: 1;
          position: relative;
        }
        .our-team .picture::before {
          content: "";
          width: 100%;
          height: 0;
          border-radius: 50%;
          background-color: #1369ce;
          position: absolute;
          bottom: 135%;
          right: 0;
          left: 0;
          opacity: 0.9;
          transform: scale(3);
          transition: all 0.3s linear 0s;
        }
        
        .our-team:hover .picture::before {
          height: 100%;
        }
        
        .our-team .picture::after {
          content: "";
          width: 100%;
          height: 100%;
          border-radius: 50%;
          background-color: #1369ce;
          position: absolute;
          top: 0;
          left: 0;
          z-index: -1;
        }
        
        .our-team .picture img {
          width: 100%;
          height: auto;
          border-radius: 50%;
          transform: scale(1);
          transition: all 0.9s ease 0s;
        }
        
        .our-team:hover .picture img {
          box-shadow: 0 0 0 14px #f7f5ec;
          transform: scale(0.7);
        }
        
        .our-team .title {
          display: block;
          font-size: 15px;
          color: #4e5052;
          text-transform: capitalize;
        }

    </style>
    """)
    st.html(f"""
        <div class="col-12 col-sm-6 col-md-4 col-lg-3">
      <div class="our-team">
        <div class="picture">
          <img class="img-fluid" src='data:image/png;base64,{imageUrl}'">
        </div>
        <div class="team-content">
          <h3 class="name" style="color: #31333F;text-transform: capitalize; font-size: 20px;">{ftname} {lname}</h3>
          <h4 class="title">{role}</h4>
        </div>
      </div>
    </div>
    """)
col1,col2,col3 = st.columns(3)
with col1:
    profilCard("youssef","bouchti",img_to_base64("assets/5.png"),"tester")
with col2:
    profilCard("youssef","bouchti",img_to_base64("assets/5.png"),"tester")
with col3:
    profilCard("youssef", "bouchti", img_to_base64("assets/5.png"), "tester")


def map():
    logiLatitTable = conn.query("SELECT longi,lati FROM VILLE")
    df = pd.DataFrame(logiLatitTable)
    st.write(df)
    col1,col2,col3 = st.columns(3)
    for index,row in df.iterrows():
        m = folium.Map(location=[row["lati"],row["longi"]], zoom_start=16)
        folium.Marker([row["lati"],row["longi"]], popup="Liberty Bell", tooltip="Liberty Bell").add_to(m)

         # call to render Folium map in Streamlit
        st_data = st_folium(m, width=725)

