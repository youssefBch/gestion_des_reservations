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
villes = conn.query("SELECT DISTINCT(nom_ville) FROM VILLE")
options = villes['nom_ville'].to_list()
selection = st.pills("Vile :", options, selection_mode="multi")
if(not(selection)):
    st.subheader("Agences de Voyage Disponibles")
    df_agenceMpa = conn.query(
        "SELECT code_a,telephone,site_web,Adresse_rue_a,Adresse_code_postal,Adresse_pays_a,VILLE_nom_ville,longi,lati FROM AGENCE_DE_VOYAGE as agence,(SELECT longi,lati,nom_ville FROM VILLE) as ville_project WHERE agence.VILLE_nom_ville = ville_project.nom_ville")
else:
    selected = tuple(selection)
    if(len(selected) == 1):
        selected = f"('{selected[0]}')"
        st.subheader(f"Agences de Voyage Disponibles a {selection[0]}")
    else:
        st.subheader(f"Agences de Voyage Disponibles a {' ,'.join(selected)}")
    df_agenceMpa = conn.query(
        f"SELECT code_a,telephone,site_web,Adresse_rue_a,Adresse_code_postal,Adresse_pays_a,VILLE_nom_ville,longi,lati FROM AGENCE_DE_VOYAGE as agence,(SELECT longi,lati,nom_ville FROM VILLE) as ville_project WHERE agence.VILLE_nom_ville = ville_project.nom_ville AND VILLE_nom_ville in {selected }")
df_agences = conn.query("SELECT * FROM AGENCE_DE_VOYAGE")

def agenceDesin1():
    for index, row in df_agences.iterrows():
        # Séparateur vide entre les agences
        st.markdown(f"""
        <div style="
            height:10px;                 /* hauteur du séparateur */
            background-color:#1b3a2d;    /* couleur sombre */
            margin-bottom:10px;          /* espace avant le contenu */
            border-radius:5px;           /* coins arrondis */
        ">
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            st.markdown(f"**Code Agence :** {row['code_a']}")

        with col2:
            st.markdown(f"**Téléphone :** {row['telephone']}")
            st.markdown(f"**Site Web :** <a href='{row['site_web']}' target='_blank'>{row['site_web']}</a>", unsafe_allow_html=True)
            st.markdown(f"**Adresse :** {row['Adresse_rue_a']}, {row['Adresse_code_postal']}, {row['Adresse_pays_a']}")
            st.markdown(f"**Ville :** {row['VILLE_nom_ville']}")

        with col3:
            st.button("Réserver", key=f"btn_{index}")


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
        </div>
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
        m = folium.Map(location=[row["lati"], row["longi"]], zoom_start=6,height="210px",position="centre",)
        # Add markers for each city
        folium.Marker([row["lati"], row["longi"]], popup="Liberty Bell",tooltip="Liberty Bell").add_to(m)
        cardAgence(row["code_a"], row["telephone"], row["site_web"], row["Adresse_rue_a"], row["VILLE_nom_ville"], m)
    if i == 1:
        i = 0
    else:
        i = i + 1
