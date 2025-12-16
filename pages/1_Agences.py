import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import text
import folium
from streamlit_folium import st_folium
from connectionDB import *
from headEdite import *
headerEdit()
st.set_page_config(page_title = "Welcome To agencies page")

st.sidebar.success("Select Any Page from here")
villes = conn.query("SELECT DISTINCT(Name) FROM CITY")
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
df_agences = conn.query("SELECT * FROM TRAVEL_AGENCY")


def cardAgence(code_a,telephone,site_web,Adresse_rue_a,VILLE_nom_ville,map):
    st.html("""
    <style>
        .property-card{
          width:360px;
          border-radius:16px;
          overflow:hidden;
          box-shadow: 0 10px 30px rgba(20,30,70,0.08);
          transition:transform .25s ease, box-shadow .25s ease;
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
            color: #f4f4f4 !important;
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
    st_folium(m,height=210)
    st.html(f"""
        <div>
        <div class="property-card">
          <div class="card-body">
            <h3 class="title">Code agence {code_a}</h3>
            <ul class="meta">
              <li>📍 {Adresse_rue_a} </li>
              <li> 📍{VILLE_nom_ville}</li>
              <li>📞 {telephone}</li>
              <li>🌐 {site_web}</li>
            </div>
          </div>
        </div>
    """)
cols = st.columns(2)
i = 0
for index, row in df_agenceMpa.iterrows():
    with cols[i]:
        m = folium.Map(location=[row["Latitude"], row["Longitude"]], zoom_start=6,height="210px",position="centre",)
        # Add markers for each city
        folium.Marker([row["Latitude"], row["Longitude"]], popup="Liberty Bell",tooltip="Liberty Bell").add_to(m)
        cardAgence(row["CodA"], row["Tel"], row["WebSite"], row["Street_Address"], row["Name"], m)
    if i == 1:
        i = 0
    else:
        i = i + 1
