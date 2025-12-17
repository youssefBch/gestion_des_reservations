import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import text
import folium
from streamlit_folium import st_folium
from connectionDB import *
from headEdite import *

headerEdit()
st.set_page_config(page_title = "Welcome To agencies page",layout="wide", initial_sidebar_state="expanded")

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

villes = conn.query("SELECT DISTINCT(Name) FROM CITY c, TRAVEL_AGENCY t WHERE c.Name=t.City_Address")
options = villes['Name'].to_list()
selection = st.pills("Ville :", options, selection_mode="multi")
if(not(selection)):
    st.subheader("Agences de Voyage Disponibles")
    df_agenceMpa = conn.query(
        "SELECT CodA,Tel,WebSite,Street_Address,ZIP_Address,Country_Address,Name,Longitude,Latitude FROM TRAVEL_AGENCY as agence,(SELECT Longitude,Latitude,Name FROM CITY) as ville_project WHERE agence.City_Address = ville_project.Name")
else:
    selected = tuple(selection)
    if(len(selected) == 1):
        selected = f"('{selected[0]}')"
        st.subheader(f"Agences de Voyage Disponibles a {selection[0]}")
    else:
        st.subheader(f"Agences de Voyage Disponibles a {' ,'.join(selected)}")
    df_agenceMpa = conn.query(
        f"SELECT CodA,Tel,WebSite,Street_Address,ZIP_Address,Country_Address,Name,Longitude,Latitude FROM TRAVEL_AGENCY as agence,(SELECT Longitude,Latitude,Name FROM CITY) as ville_project WHERE agence.City_Address = ville_project.Name AND Name in {selected }")


def cardAgence(code_a,telephone,site_web,Adresse_rue_a,VILLE_nom_ville):
    st.html("""
    <style>
        .property-card{
        border: 1px solid #ffffff21;
            display: flex;
    align-items: flex-start;
          width:100%;
          height:150px;
          border-radius:16px;
          overflow:hidden;
          box-shadow: 0 10px 30px rgba(20,30,70,0.08);
          transition:transform .25s ease, box-shadow .25s ease;
        }
        .property-card:before {
            content: "";
            position: absolute;
            background-color: #1369ce;
          position: absolute;
          width: 100%;
        height: 0px;
          bottom: 0px;
          right: 0px;
          opacity: 0.9;
            border-radius: 0%;
          transform: scale(0);
          transition: all 0.4s linear 0s;
        }
        .property-card:hover:before{
            transform: scale(2);
            height: 7px;
            border-radius: 50%;
        }
        .property-card:hover{
          transform:translateY(-8px);
          box-shadow: 0 20px 50px rgba(20,30,70,0.12);
        }
        .property-map{
          width:100%;
          height:200px;
          object-fit:cover;
          display:block;
        }
        .card-body{
          padding:18px;
        }
        .card-body .title{
              margin: 0 0 8px 0;
            font-size: 18px;
            color: var(--muted) !important;
        }
        
        .meta {
            display: flex;
            gap: 16px;
            color: var(--muted);
            font-size: 13px;
            margin-bottom: 14px;
            flex-direction: row;
            flex-wrap: wrap;
            justify-content: space-between;
            list-style: none;
        }
    </style>
    """)
    st.html(f"""
        <div>
        <div class="property-card">
          <div class="card-body">
            <h3 class="title">Code agence {code_a}</h3>
            <ul class="meta">
              <li>📍 {Adresse_rue_a} </li>
              <li> 📍{VILLE_nom_ville}</li>
              <li>📞 {telephone}</li>
              <li>
                  <a href="{site_web}" target="_blank">{site_web}</a>
              </li>
            </div>
          </div>
        </div>
    """)
st.space(size="small")
cols = st.columns(3,gap="medium")
i = 0
for index, row in df_agenceMpa.iterrows():
    with cols[i]:
        if row["WebSite"] == None:
            row["WebSite"] = ''
        else:
            row["WebSite"] = f"🌐 {row['WebSite']}"
        cardAgence(row["CodA"], row["Tel"], row["WebSite"], row["Street_Address"], row["Name"])
    if i == 2:
        i = 0
    else:
        i = i + 1



# Center map on the average location

avg_lat = df_agenceMpa['Latitude'].mean()
avg_long = df_agenceMpa['Longitude'].mean()
m = folium.Map(location=[avg_lat, avg_long], zoom_start=6)
# Add markers for each city
for index,row in df_agenceMpa.iterrows():
    popup_content = f"""
        <a href="){row["WebSite"]}" target="_blank">
            {row["WebSite"]}
        </a>
    """
    tooltip_content = f"""
        <b>{row['Name']}</b><br>
        <i>Agence {row['CodA']}</i>
        """
    folium.Marker(
        [row["Latitude"],row["Longitude"]],
        popup=popup_content,
        tooltip=tooltip_content,
    ).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)