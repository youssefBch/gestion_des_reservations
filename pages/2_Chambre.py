import streamlit as st
import pandas as pd
from connectionDB import *
import streamlit.components.v1 as components
import base64
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
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ==============================
# FILTRES
# ==============================
st.subheader("Filtres")

col1, col2, col3 = st.columns(3)

with col1:
    type_filtre = st.radio(
        "Type de chambre",
        ["All", "Single", "Double", "Suite"]
    )

with col2:
    options_filtre = st.multiselect(
        "Amenities",
        ["balcony", "jacuzzi", "minibar", "pay-tv"]
    )

with col3:
    cuisine_filtre = st.checkbox("With kitchen")

# ==============================
# APPLICATION DES FILTRES
# ==============================

df_filtre = conn.query(f"""
        SELECT *
        FROM ROOM
    """)

radioSelected = ('suite','double','single')
if type_filtre != "All":
    radioSelected = f"('{type_filtre.lower()}')"
    df_filtre = conn.query(f"""
        SELECT r.*
        FROM ROOM r
        WHERE r.Type IN {radioSelected};
    """)

selected = ("balcony", "jacuzzi", "minibar", "pay-tv")

if options_filtre:
    selected = tuple(options_filtre)
    if len(selected) == 1:
        selected = f"('{selected[0]}')"   # avoid getting a tuple with this form (tuple_value,)
        countSelected = 1
    else:
        countSelected = len(selected)

    df_filtre = conn.query(f"""
        SELECT  q1.CodR, count(q1.AMENITIES_Amenity),q1.SurfaceArea, q1.Type
        
        FROM( 	SELECT *
                FROM ( SELECT r.*
                FROM ROOM r
                WHERE r.Type IN {radioSelected}
                ) r1
                JOIN HAS_AMENITIES ha ON ha.ROOM_CodR = r1.CodR
                WHERE ha.AMENITIES_Amenity IN {selected}
        ) q1
        GROUP BY q1.CodR
        HAVING count(q1.AMENITIES_Amenity) = {countSelected};
    """)


# Filtre cuisine
if cuisine_filtre:
    if options_filtre:
        selected = tuple(options_filtre)
        if len(selected) == 1:
            selected = f"('{selected[0]}')"  # avoid getting a tuple with this form (tuple_value,)
            countSelected = 1
        else:
            countSelected = len(selected)

        df_filtre = conn.query(f"""
            SELECT  q1.CodR, count(q1.AMENITIES_Amenity),q1.SurfaceArea, q1.Type

            FROM( 	SELECT *
                    FROM ( SELECT r.*
                    FROM ROOM r
                    WHERE r.Type IN {radioSelected}
                    ) r1
                    JOIN HAS_AMENITIES ha ON ha.ROOM_CodR = r1.CodR
                    JOIN HAS_SPACES h ON h.ROOM_CodR = r1.CodR
                    WHERE ha.AMENITIES_Amenity IN {selected}
                    AND SPACES_Space = "kitchen"
            ) q1
            GROUP BY q1.CodR
            HAVING count(q1.AMENITIES_Amenity) = {countSelected};
        """)

    else :
        df_filtre = conn.query(f"""
            SELECT  DISTINCT(q1.CodR),q1.SurfaceArea, q1.Type

            FROM( 	SELECT *
                    FROM ( SELECT r.*
                    FROM ROOM r
                    WHERE r.Type IN {radioSelected}
                    ) r1
                    JOIN HAS_AMENITIES ha ON ha.ROOM_CodR = r1.CodR
                    JOIN HAS_SPACES h ON h.ROOM_CodR = r1.CodR
                    WHERE ha.AMENITIES_Amenity IN {selected}
                    AND SPACES_Space = "kitchen"
            ) q1
            
        """)

# ==============================
# AFFICHAGE TABLE
# ==============================
st.subheader("Chambres disponibles (Table)")
st.dataframe(
    df_filtre[["CodR", "SurfaceArea", "Type"]],
    use_container_width=True
)


def cardChambre(code_c, surface, type_chambre):
    st.html("""
    <style>
        .property-card{
            border: 1px solid #ffffff21;
            display: flex;
         align-items: flex-start;
width:100%;            height: 320px;
          border-radius:16px;
          overflow:hidden;
          box-shadow: 0 10px 30px rgba(20,30,70,0.08);
          transition:transform .25s ease, box-shadow .25s ease;
        }
        .property-card:hover{
          transform:translateY(-8px);
          box-shadow: 0 20px 50px rgba(20,30,70,0.12);
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
        .card-body{
          padding:18px;
        }
        .card-body .title{
              margin: 0 0 8px 0;
            font-size: 18px;
            color: var(--muted);
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
        .card-image{
            width:100%;
            border-radius: 5px;
        }
    </style>
    """)

    if type_chambre == "suite":
        image_html = f'<img class="card-image" src="data:image/png;base64,{img_to_base64("assets/bg6.jpg")}" style="width:100%">'
    elif type_chambre == "double":
        image_html = f'<img class="card-image" src="data:image/png;base64,{img_to_base64("assets/bg7.jpg")}" style="width:100%">'
    elif type_chambre == "single":
        image_html = f'<img class="card-image" src="data:image/png;base64,{img_to_base64("assets/bg9.jpg")}" style="width:100%">'
    st.html(f"""
        <div class="property-card">
            <div class="card-body">
                {image_html}
                <h3 class="title">Code chambre {code_c}</h3>
                <ul class="meta">
                    <li>Surface : {surface}</li>
                    <li>Type de chambre : {type_chambre}</li>
                </ul>
            </div>
        </div>
    """)


cols = st.columns(3)
i = 0
for index, row in df_filtre.iterrows():
    with cols[i]:
        cardChambre(row["CodR"], row["SurfaceArea"], row["Type"])
    if i == 2:
        i = 0
    else:
        i = i + 1
