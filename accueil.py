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
st.set_page_config(page_title = "Welcome To our reservation web site")
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def heroSection(imageUrl,title,undertitle):
    st.html("""
    <style>
    
    .glass-card {
      background: rgba(255, 255, 255, 0.1);
      border-radius: 16px;
      padding: 40px;
      max-width: 500px;
      width: 90%;
      backdrop-filter: blur(15px);
      -webkit-backdrop-filter: blur(15px);
      box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      text-align: center;
      color: white;
    }
    
    .glass-card h1 {
      font-size: 2.5rem;
      margin-bottom: 20px;
    }
    
    .glass-card p {
      font-size: 1.1rem;
      margin-bottom: 30px;
    }
    
    .glass-card button {
      padding: 12px 25px;
      border: none;
      background: rgba(255, 255, 255, 0.3);
      color: white;
      font-size: 1rem;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.3s ease;
    }
    
    .glass-card button:hover {
      background: rgba(255, 255, 255, 0.5);
    }
    
    .more-section {
      padding: 60px 20px;
      text-align: center;
      background: white;
      color: #333;
    }
    </style>
        """)
    st.html(f"""
        <section class="hero" style="height: 90vh;
        border-radius: 50px;
      display: flex;
      justify-content: center;
      align-items: center;
      background-image: url('data:image/png;base64,{imageUrl}');
      background-size: cover;
      background-position: center;
      position: relative;">
          <div class="glass-card">
            <h1>{title}</h1>
            <p>{undertitle}</p>
          </div>
        </section>

    """)

with st.container():
    heroSection(img_to_base64("assets/bg.jpg"),"hello","h")

st.space(size="medium")


st.subheader("Notre hotels")
st.space(size="small")


def stasCard(nbr,title,icon):
    st.html("""
        <style>
            .stat-card {
              background-color: #d6eaff;
              flex: 1;
              min-width: 180px;
              max-width: 220px;
              background-color: #eee;
              border-radius: 15px;
              padding: 20px;
              text-align: center;
              box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            }
            
            .icon {
              background-color: rgba(0, 102, 204, 0.15);
              color: #004c99;
              font-size: 24px;
              width: 40px;
              height: 40px;
              margin: 0 auto 10px;
              line-height: 40px;
              border-radius: 50%;
              background-color: rgba(0, 0, 0, 0.08);
            }
            
            .value {
              font-size: 22px;
              font-weight: bold;
              margin-bottom: 5px;
              color: #002d66;
            }
            
            .label {
              font-size: 13px;
              color: #555;
            }

        </style>
    """)
    st.html(f"""
      <div class="stat-card">
        <div class="icon">{icon}</div>
        <div class="value">{nbr}</div>
        <div class="label">{title}</div>
      </div>
""")
col1,col2,col3 = st.columns(3)
nbrAgance = conn.query("SELECT count(*) as nrbAgance FROM AGENCE_DE_VOYAGE")["nrbAgance"][0]
nbrVille = conn.query("SELECT count(*) as nbrVille FROM VILLE")["nbrVille"]
nbrResevation = conn.query("SELECT count(*) as nbrResevation FROM RESERVATION")["nbrResevation"][0]
with col1:
    stasCard(nbrAgance, "nombres des agence", "🏢")
with col2:
    stasCard(nbrAgance, "nombres des agence", "🏢")
with col3:
    stasCard(nbrAgance, "nombres des agence", "🏢")
st.space(size="medium")
st.subheader("Notre team")
st.space(size="small")
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

