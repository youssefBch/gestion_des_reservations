import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import text
from connectionDB import *
from headEdite import *
headerEdit()

df_reservation = conn.query("""
SELECT 
    r1.CHAMBRE_code_c, 
    c.surface,
    DATE_FORMAT(r1.data_d, '%Y-%m-01') AS mois, 
    AVG(r1.prix) AS avg_prix
FROM RESERVATION r1
JOIN CHAMBRE c ON c.code_c = r1.CHAMBRE_code_c
GROUP BY r1.CHAMBRE_code_c, mois
HAVING AVG(r1.prix) = (
    SELECT MAX(sub.avg_prix)
    FROM (
        SELECT 
            r2.CHAMBRE_code_c, 
            DATE_FORMAT(r2.data_d, '%Y-%m-01') AS mois1, 
            AVG(r2.prix) AS avg_prix
        FROM RESERVATION r2
        GROUP BY r2.CHAMBRE_code_c, mois1
    ) sub
    WHERE sub.mois1 = mois
);

""")

df_suite = conn.query("SELECT * FROM SUITE")
def get_type(row):
    if row['CHAMBRE_code_c'] in df_suite['CHAMBRE_code_c'].values:
        return 'Suite'
    elif row['surface'] <= 25:
        return 'Simple'
    elif row['surface'] <= 50:
        return 'Double'
    else:
        return 'Triple'


df_reservation['type_chambre'] = df_reservation.apply(get_type, axis=1)
st.write(df_reservation)