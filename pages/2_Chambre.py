import streamlit as st
import pandas as pd
from connectionDB import *
import streamlit.components.v1 as components
import base64

st.header("Page Chambres")
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

df_chambre = conn.query("""
SELECT *
FROM CHAMBRE c
LEFT JOIN HAS_EQUIPEMENT h ON h.CHAMBRE_code_c = c.code_c;
""")

df_suite = conn.query("SELECT * FROM SUITE")
def get_type(row):
    if row['code_c'] in df_suite['CHAMBRE_code_c'].values:
        return 'Suite'
    elif row['surface'] <= 25:
        return 'Simple'
    elif row['surface'] <= 50:
        return 'Double'
    else:
        return 'Triple'

df_chambre['type_chambre'] = df_chambre.apply(get_type, axis=1)

# Grouper tous les équipements par chambre
df_equipements = df_chambre.groupby('code_c')['EQUIPEMENT_equipement'].apply(list).reset_index()

# Conserver les colonnes de surface et type_chambre
df_chambre_unique = df_chambre[['code_c','surface','type_chambre']].drop_duplicates()
df_chambre_grouped = df_chambre_unique.merge(df_equipements, on='code_c', how='left')

# ==============================
# FILTRES
# ==============================
st.subheader("Filtres")

col1, col2, col3 = st.columns(3)

with col1:
    type_filtre = st.radio(
        "Type de chambre",
        ["Toutes", "Simple", "Double", "Triple"]
    )

with col2:
    options_filtre = st.multiselect(
        "Options",
        ["WiFi", "TV", "Balcon"]
    )

with col3:
    cuisine_filtre = st.checkbox("Avec cuisine")

# ==============================
# APPLICATION DES FILTRES
# ==============================
df_filtre = df_chambre_grouped.copy()

if type_filtre != "Toutes":
    df_filtre = df_filtre[df_filtre["type_chambre"] == type_filtre]

if type_filtre == "Toutes":
    df_filtre = df_filtre[df_filtre["type_chambre"] != "Suite"]

if options_filtre:
    df_filtre = df_filtre[
        df_filtre["EQUIPEMENT_equipement"].apply(
            lambda x: all(opt in x for opt in options_filtre)
        )
    ]


# Filtre cuisine
if cuisine_filtre:
    df_filtre = df_filtre[df_filtre['EQUIPEMENT_equipement'].apply(lambda x: 'Cuisine' in x)]

# ==============================
# AFFICHAGE TABLE (OBLIGATOIRE)
# ==============================
st.subheader("Chambres disponibles (Table)")
st.dataframe(
    df_filtre[["code_c", "surface", "type_chambre"]],
    use_container_width=True
)


def cardChambre(code_c, surface, type_chambre):
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
            <img class="mySlides" src="data:image/png;base64,{img_to_base64("assets/bg1.jpg")}" style="width:100%">
            <h3 class="title">Code chambre {code_c}</h3>
            <ul class="meta">
              <li>Surface : {surface}</li>
              <li>Type de chambre : {type_chambre}</li>
            </div>
          </div>
        </div>
    """)


cols = st.columns(2)
i = 0
for index, row in df_filtre.iterrows():
    with cols[i]:
        cardChambre(row["code_c"], row["surface"], row["type_chambre"])
    if i == 1:
        i = 0
    else:
        i = i + 1
