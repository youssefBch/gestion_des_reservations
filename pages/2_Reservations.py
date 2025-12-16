import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import text
from connectionDB import *
from headEdite import *
headerEdit()
st.set_page_config(page_title = "Welcome to the Booking Information Page")

st.set_page_config(page_title="Welcome To our reservation web site", layout="wide", initial_sidebar_state="expanded")

df_reservation = conn.query("""

SELECT 
    DATE_FORMAT(b1.StartDate, '%Y-%m-01') AS month,
    b1.ROOM_CodR,
    AVG(b1.Cost) AS avg_Cost,
    r.Floor,
    r.SurfaceArea, 
    r.Type
FROM BOOKING b1
JOIN ROOM r ON r.CodR = b1.ROOM_CodR
GROUP BY b1.ROOM_CodR, month
HAVING AVG(b1.Cost) = (
    SELECT MAX(sub.avg_Cost)
    FROM (
        SELECT 
            b2.ROOM_CodR, 
            DATE_FORMAT(b2.StartDate, '%Y-%m-01') AS month1, 
            AVG(b2.Cost) AS avg_Cost
        FROM BOOKING b2
        GROUP BY b2.ROOM_CodR, month1
    ) sub
    WHERE sub.month1 = month
);
""")

# Principal DataFrame
df_reservation["Month"] = pd.to_datetime(df_reservation['month']).dt.month_name()
df_reservation.drop(columns='month', inplace=True)

options = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
selection = st.pills("months :", options, selection_mode="multi")

if(not(selection)):
    st.subheader("Chambre ayant le coût journalier moyen le plus élevé par mois")
    df_reservations_display = df_reservation
else:
    selected = list(selection)
    if(len(selected) == 1):
        nombre_chambre = len(df_reservation[df_reservation['Month'] == selected[0]])
        st.subheader(f"Chambre ayant le coût journalier moyen le plus élevé en {selection[0]} ({nombre_chambre}) :")
    else:
        nombre_chambre = len(df_reservation[df_reservation['Month'].isin(selected)])
        st.subheader(f"Chambre ayant le coût journalier moyen le plus élevé en {', '.join(selected)} ({nombre_chambre}) :")

    df_reservations_display = df_reservation[df_reservation['Month'].isin(selected)]


def cardChambre(Room_CodR, SurfaceArea, Type, Floor):
    st.html("""
    <style>
        .property-card{
          width:360px;
          height:150px;
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
    st.html(f"""
        <div>
        <div class="property-card">
          <div class="card-body">
            <h3 class="title">Code chambre {Room_CodR}</h3>
            <ul class="meta">
              <li><h4>Type : {Type} </h4></li>
              <li><h4>Floor : {Floor} </h4></li>
              <li><h4>Area : {SurfaceArea} </h4></li>
            </div>
          </div>
        </div>
    """)


cols = st.columns(1)
with cols[0]:
    for index, row in df_reservations_display.iterrows():
            cardChambre(row["ROOM_CodR"], row["SurfaceArea"], row["Type"], row["Floor"])
