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

st.markdown(
        """
        <style>
        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #262730 !important;
        }

        /* Sidebar text color */
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        /* Header / navbar background */
        header {
            background-color: #0E1117 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def heroSection(*args):
    import streamlit.components.v1 as components

    html_code = f"""
    <style>
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}

    .slideshow-container {{
        position: relative;
        width: 100%;
        height: 100vh;
        overflow: hidden;
        border-radius: 12px;
    }}

    .mySlides {{
        display: none;
        width: 100%;
        height: 600px;
        object-fit: cover;
        filter: brightness(0.45);
    }}

    /* HERO OVERLAY */
    .hero-overlay {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        color: white;
        max-width: 900px;
        padding: 20px;
    }}

    .hero-label {{
        letter-spacing: 2px;
        font-size: 14px;
        color: #d4af37;
        margin-bottom: 15px;
        text-transform: uppercase;
    }}

    .hero-title {{
        font-size: 56px;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 15px;
    }}

    .hero-subtitle {{
        font-size: 22px;
        margin-bottom: 20px;
        opacity: 0.95;
    }}

    .hero-description {{
        font-size: 16px;
        line-height: 1.7;
        opacity: 0.9;
        margin-bottom: 35px;
    }}

    .hero-buttons {{
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
    }}

    .hero-btn {{
        padding: 14px 28px;
        font-size: 15px;
        border-radius: 6px;
        border: none;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
    }}

    .btn-primary {{
        background-color: #d4af37;
        color: #111;
    }}

    .btn-primary:hover {{
        background-color: #b8962e;
    }}

    .btn-secondary {{
        background-color: transparent;
        border: 2px solid #fff;
        color: #fff;
    }}

    .btn-secondary:hover {{
        background-color: #fff;
        color: #111;
    }}
    </style>

    <div class="slideshow-container">
        <img class="mySlides" src="data:image/png;base64,{img_to_base64(args[0])}">
        <img class="mySlides" src="data:image/png;base64,{img_to_base64(args[1])}">
        <img class="mySlides" src="data:image/png;base64,{img_to_base64(args[2])}">

        <div class="hero-overlay">
            <div class="hero-label">— Premium Hotel Experience —</div>

            <div class="hero-title">
                Experience Comfort, Elegance <br>& Serenity
            </div>

            <div class="hero-subtitle">
                A refined stay designed for unforgettable moments
            </div>

            <div class="hero-description">
                Discover a modern hotel management platform where luxury meets simplicity.
                Explore elegant rooms, manage reservations effortlessly, and enjoy a seamless
                experience tailored for your comfort.
            </div>

            <div class="hero-buttons">
                <button class="hero-btn btn-primary">Explore Rooms</button>
                <button class="hero-btn btn-secondary">Check Availability</button>
            </div>
        </div>
    </div>

    <script>
    let slideIndex = 0;
    showSlides();

    function showSlides() {{
        let slides = document.getElementsByClassName("mySlides");

        for (let i = 0; i < slides.length; i++) {{
            slides[i].style.display = "none";
        }}

        slideIndex++;
        if (slideIndex > slides.length) {{ slideIndex = 1 }}

        slides[slideIndex - 1].style.display = "block";
        setTimeout(showSlides, 3000);
    }}
    </script>
    """

    components.html(html_code, height=650)


heroSection("assets/bg1.jpg", "assets/bg2.jpg", "assets/bg3.jpg")

st.space(size="medium")

st.subheader("Hotel Summary")
st.space(size="small")


def stasCard(nbr, title, icon):
    st.html("""
        <style>
        /*****
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
***/
            .card {
            width:100%;
            background-color: #ffffff;
            border-radius: 0.5rem;
            border: 1px solid rgb(163 168 184 / 37%);
            padding: 1.5rem;
            position: relative;
            overflow: hidden;
            transition:transform .25s ease, box-shadow .25s ease;
        }
    .card:hover{
          transform:translateY(-8px);
          box-shadow: 0 20px 50px rgba(20,30,70,0.12);
        }
        .card dt {
            font-size: 01rem;
            font-weight: 500;
            color: #6b7280; /* gray-500 */
            margin-bottom: 0.5rem;
        }

        .card dd {
            font-size: 2rem;
            font-weight: 600;
            color: #d4af37;
        }
        .card:before {
            content: "";
            position: absolute;
            background-color: #b8962e;
          position: absolute;
          width: 100px;
        height: 100%;
          bottom: 0;
          right: -100px;
          opacity: 0.9;
            border-radius: 0%;
          transform: scale(0);
          transition: all 0.4s linear 0s;
        }
        .card:hover:before{
            transform: scale(2);
            border-radius: 50%;
        }
        </style>
    """)
    st.html(f"""
      <!--div class="stat-card">
        <div class="icon">{icon}</div>
        <div class="value">{nbr}</div>
        <div class="label">{title}</div>
      </div--->
                  <div class="card">
                <dl>
                    <dt>{title}</dt>
                    <dd>{nbr}</dd>
                </dl>
            </div>
""")
col1,col2,col3 = st.columns(3)
nbrBOOKING = conn.query("SELECT count(*) as nbrBOOKING FROM BOOKING")["nbrBOOKING"][0]
nbrRoom = conn.query("SELECT count(*) as nbrRoom FROM ROOM")["nbrRoom"][0]
nbrAumnities = conn.query("SELECT count(*) as nbrAmni FROM HAS_AMENITIES")["nbrAmni"][0]
with col1:
    stasCard(nbrBOOKING, "Total Reservations", "🏢")
with col2:
    stasCard(nbrRoom, "Total Rooms", "🏢")
with col3:
    stasCard(nbrAumnities, "Total Amenities", "🏢")
st.space(size="medium")
st.subheader("Our Team")
st.space(size="small")


def profilCard(ftname, lname, imageUrl, role):
    st.html("""
    <style>
    .our-team {
            width:100%;
          padding: 30px 0 40px;
          margin-bottom: 30px;
          background-color: #fffcf3;
          text-align: center;
          border-radius: 10px;
          width:100%;
          overflow: hidden;
          position: relative;
          transition:transform .25s ease, box-shadow .25s ease;
        }
    .our-team:hover{
          transform:translateY(-8px);
          box-shadow: 0 20px 50px rgba(20,30,70,0.12);
        }
        .our-team .picture {
          display: inline-block;
          width: 100px;
            height: 100px;
            margin: 0;
          z-index: 1;
          position: relative;
        }
        .our-team .picture::before {
          content: "";
          width: 100%;
          height: 0;
          border-radius: 50%;
        background-color: #b8962e;
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
        <div style="
    width:100%;
    /* height: 136px; */
">
      <div class="our-team"style="
        background-color: rgb(255 255 255);">
        <div class="picture">
          <img class="img-fluid" src='data:image/png;base64,{imageUrl}'">
        </div>
        <div class="team-content">
          <h3 class="name" style="color: #31333F;text-transform: capitalize; font-size: 20px;color: #31333F;
    text-transform: capitalize;
    font-size: 20px;
    margin: 15px 0px 5px 0px;">{ftname} {lname}</h3>
        </div>
      </div>
    </div>
    """)


col1, col2, col3, col4 = st.columns(4,gap='small')
with col1:
    profilCard("Youssef", "Bouchti", img_to_base64("assets/12.png"), "tester")
with col2:
    profilCard("Amine", "El Asri", img_to_base64("assets/12.png"), "tester")
with col3:
    profilCard("Zainab", "Rezoukia", img_to_base64("assets/66.png"), "tester")
with col4:
    profilCard("Badr", "El majdoub", img_to_base64("assets/12.png"), "tester")
with col1:
    profilCard("Najoua", "Horma", img_to_base64("assets/66.png"), "tester")
with col2:
    profilCard("Chaimae", "Ghonim", img_to_base64("assets/66.png"), "tester")
with col3:
    profilCard("Mariem", "Sidi", img_to_base64("assets/66.png"), "tester")




