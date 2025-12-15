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

def heroSection(*args):
    import streamlit.components.v1 as components

    html_code = f"""
    <style>
    * {{box-sizing: border-box;}}
    body {{font-family: Verdana, sans-serif;}}
    .mySlides {{display: none;}}
    img {{vertical-align: middle;}}

    .slideshow-container {{
      max-width: 1000px;
      position: relative;
      margin: auto;
      border-radius: 10px
    }}

    .dot {{
      height: 15px;
      width: 15px;
      margin: 0 2px;
      background-color: #bbb;
      border-radius: 50%;
      display: inline-block;
    }}

    .active {{
      background-color: #717171;
    }}
    </style>

    <div class="slideshow-container">
      <img class="mySlides" src="data:image/png;base64,{img_to_base64(args[0])}" style="width:100%">
      <img class="mySlides" src="data:image/png;base64,{img_to_base64(args[1])}" style="width:100%">
      <img class="mySlides" src="data:image/png;base64,{img_to_base64(args[2])}" style="width:100%">
    </div>

    <div style="text-align:center">
      <span class="dot"></span>
      <span class="dot"></span>
      <span class="dot"></span>
    </div>

    <script>
    let slideIndex = 0;
    showSlides();

    function showSlides() {{
      let slides = document.getElementsByClassName("mySlides");
      let dots = document.getElementsByClassName("dot");

      for (let i = 0; i < slides.length; i++) {{
        slides[i].style.display = "none";
      }}

      slideIndex++;
      if (slideIndex > slides.length) {{slideIndex = 1}}

      for (let i = 0; i < dots.length; i++) {{
        dots[i].className = dots[i].className.replace(" active", "");
      }}

      slides[slideIndex - 1].style.display = "block";
      dots[slideIndex - 1].className += " active";

      setTimeout(showSlides, 2000);
    }}
    </script>
    """

    components.html(html_code, height=600)


heroSection("assets/bg1.jpg", "assets/bg2.jpg", "assets/bg3.jpg")

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
nbrVille = conn.query("SELECT count(*) as nbrVille FROM VILLE")["nbrVille"][0]
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
    profilCard("Youssef","Bouchti",img_to_base64("assets/5.png"),"tester")
with col2:
    profilCard("Amine","El Asri",img_to_base64("assets/5.png"),"tester")
with col3:
    profilCard("youssef", "bouchti", img_to_base64("assets/5.png"), "tester")




