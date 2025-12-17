import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import text
from connectionDB import *
from headEdite import *
import base64

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

headerEdit()
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
    st.subheader("Room with the Highest Average Daily Rate per Month")
    df_reservations_display = df_reservation
else:
    selected = list(selection)
    if(len(selected) == 1):
        nombre_chambre = len(df_reservation[df_reservation['Month'] == selected[0]])
        st.subheader(f"Room with the Highest Average Daily Rate per Month in {selection[0]} ({nombre_chambre}) :")
    else:
        nombre_chambre = len(df_reservation[df_reservation['Month'].isin(selected)])
        st.subheader(f"Room with the Highest Average Daily Rate per Month in {', '.join(selected)} ({nombre_chambre}) :")

    df_reservations_display = df_reservation[df_reservation['Month'].isin(selected)]


def cardChambre(Room_CodR, SurfaceArea, Type, Floor):
    st.html("""
    <style>
        .property-card{
          border: 1px solid #ffffff21;
            display: flex;
         align-items: flex-start;
          width:100%;
            height: 150px;
          border-radius:16px;
          overflow:hidden;
          box-shadow: 0 10px 30px rgba(20,30,70,0.08);
          transition:transform .25s ease, box-shadow .25s ease;
        }
        .property-card:hover:before{
            transform: scale(2);
            height: 7px;
            border-radius: 50%;
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


cols = st.columns(3)
i = 0
for index, row in df_reservations_display.iterrows():
    with cols[i]:
        cardChambre(row["ROOM_CodR"], row["SurfaceArea"], row["Type"], row["Floor"])
    if i == 2:
        i = 0
    else:
        i = i + 1
st.space(size="medium")

st.subheader("Price Variation by Month")

df = conn.query("SELECT DATE_FORMAT(StartDate, '%Y-%m-01') AS month, avg(Cost) as avg_cost FROM BOOKING group by month")
df["month"] = pd.DatetimeIndex(df["month"]).strftime('%B')
st.line_chart(
    df,
    x="month",
    y="avg_cost",
)

