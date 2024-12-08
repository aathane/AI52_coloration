# -*- coding: utf-8 -*-
"""
Created on Sat DEC 07 14:43:00 2024
Sujet  :  Coloration de graphes appliquée à la France
@author: ATHANE Augustin - VERNADE Mathias - MAURER Gilles - MEIRINHO Hugo
"""

# Import libs
import streamlit as st
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from app.RecuitSimule import RecuitSimule
from app.Genetique import Genetique
from geo_environment import GeoEnv

# Constants
COLORS_LIST = ["#FF0000", "#0000FF", "#FFFF00", "#00FF00"]

# Streamlit UI
# Title
st.markdown("""<h1 style='text-align: center; color: black;'>Coloration de Graphes : Régions Métropolitaines de France</h1><hr style='border: 2px solid blue;'>""", unsafe_allow_html=True)

# Navigation bar
add_sidebar = st.sidebar.selectbox('Choisir la page', ('Calculs', 'Algorithmes'))

# Mathematique page
if add_sidebar == 'Calculs':
    st.subheader('Calculs Mathematique pour résoudre le problème')
    st.latex(r'a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} = \sum_{k=0}^{n-1} ar^k = a \left(\frac{1-r^{n}}{1-r}\right)')

# Algorithme page
if add_sidebar == 'Algorithmes':
    st.subheader('Test et démonstration des algorithmes')
    geojson_choice = st.selectbox('Choisir une carte', ('regions', 'departements'))

    # Separate into 2 columns : 
    col1, col2 = st.columns(2)

    # Column 1: Display the map with no color
    geo_env = GeoEnv(geojson_choice)
    fig = geo_env.show_graph(title=geojson_choice)
    col1.pyplot(fig)

    # Column 2: Select the algorithm
    algo_selected = col2.selectbox('Choisir un Algorithme', ('Recuit simule', 'Algorithme genetique'))
