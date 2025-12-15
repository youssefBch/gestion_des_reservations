import streamlit as st
import pandas as pd
from connectionDB import *

st.header("Page Chambres")

# ==============================
# DONNÉES (SANS FICHIER EXTERNE)
# ==============================
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

# ==============================
# AFFICHAGE MAX 5 (FACULTATIF)
# ==============================
st.subheader("Détails des chambres (max 5)")

df_limite = df_filtre.head(5)

for index, row in df_limite.iterrows():
    st.write(f"""
    Code : {row['code_c']}    
    Superficie : {row['surface']} m²  
    Type : {row['type_chambre']}
    """)
    st.divider()