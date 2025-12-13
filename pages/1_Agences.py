import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import text
import folium
from streamlit_folium import st_folium
from connectionDB import *
st.set_page_config(page_title = "Welcome To agencies page")

st.sidebar.success("Select Any Page from here")

df_agences = conn.query("SELECT * FROM AGENCE_DE_VOYAGE")
st.subheader("Agences de Voyage Disponibles")
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