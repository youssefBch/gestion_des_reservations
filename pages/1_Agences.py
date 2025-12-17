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
st.subheader("Notre hotels")
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
nbrAgance = conn.query("SELECT count(*) as nrbAgance FROM TRAVEL_AGENCY")["nrbAgance"][0]
nbrVille = conn.query("SELECT count(*) as nbrVille FROM CITY")["nbrVille"][0]
nbrResevation = conn.query("SELECT count(CodA),City_Address FROM TRAVEL_AGENCY group by City_Address order by count(CodA) DESC")["City_Address"][0]
with col1:
    stasCard(nbrAgance, "nombres des agence", "🏢")
with col2:
    stasCard(nbrAgance, "nombres des agence", "🏢")
with col3:
    stasCard(nbrAgance, "nombres des agence", "🏢")

st.space(size="medium")
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
            background-color: #b8962e;
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