import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import text
def headerEdit():
    st.logo("assets/ensak.png",size="medium")
    st.set_page_config(page_title="Hotel App", layout="wide")

    # ---- SIDEBAR STYLE ----
    st.markdown("""
    <style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e2f, #2a2a40);
    }
    
    /* Center everything in sidebar */
    [data-testid="stSidebar"] > div:first-child {
        display: flex;
        flex-direction: column;
        justify-content: center;   /* vertical center */
        align-items: center;       /* horizontal center */
        height: 100vh;
    }
    
    /* Sidebar title */
    .sidebar-title {
        font-size: 26px;
        font-weight: bold;
        color: white;
        margin-bottom: 30px;
    }
    
    /* Radio buttons text */
    div[role="radiogroup"] > label {
        justify-content: center !important;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---- SIDEBAR CONTENT ----
    st.sidebar.markdown("<div class='sidebar-title'>🏨 Hotel Manager</div>", unsafe_allow_html=True)

    menu = st.sidebar.radio(
        "",
        ["🏠 Accueil", "🏢 Agences", "🛏️ Chambre", "📅 Réservations"],
    )

    # ---- PAGES ----
    if menu == "🏠 Accueil":
        st.title("🏠 Accueil")
        st.write("Bienvenue sur la plateforme de gestion hôtelière.")

    elif menu == "🏢 Agences":
        st.title("🏢 Agences")
        st.write("Gestion des agences partenaires.")

    elif menu == "🛏️ Chambre":
        st.title("🛏️ Chambres")
        st.write("Gestion des chambres.")

    elif menu == "📅 Réservations":
        st.title("📅 Réservations")
        st.write("Gestion des réservations.")
