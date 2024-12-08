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
COLORS_LIST = [
    "#FF0000",  # Rouge
    "#0000FF",  # Bleu
    "#FFFF00",  # Jaune
    "#00FF00",  # Vert
    "#FF00FF",  # Magenta
    "#00FFFF",  # Cyan
    "#800000",  # Marron
    "#808000",  # Olive
    "#008080",  # Turquoise foncé
    "#800080"   # Violet
]


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

    # Réinitialiser les couleurs
    solution_colors = None

    # Séparer en 2 colonnes :
    col1, col2 = st.columns(2)

    # Initialiser l'environnement et la figure sans couleur
    geo_env = GeoEnv(geojson_choice)
    adjacency_matrix, region_names = geo_env.adjacency_matrix()
    num_nodes = len(region_names)

    # Colonne 2 : Sélection de l'algorithme
    algo_selected = col2.selectbox('Choisir un Algorithme', ('Recuit simule', 'Algorithme genetique'))

    # Sélection du nombre de couleurs
    max_colors = col2.select_slider('Choisissez le nombre de couleurs :', options=list(range(1, 11)), value=4)

    expander = col2.expander("Plus de parametres")
    if algo_selected == 'Recuit simule':
        temperature_initiale = expander.number_input("Température initiale", min_value=1, value=1000, step=1)
        facteur = expander.number_input("Facteur de réduction", min_value=0.01, max_value=1.0, value=0.99, step=0.01)
        iterations = expander.number_input("Nombre d'itérations", min_value=1, value=500, step=1)
        voisinages = expander.number_input("Nombre de voisinages", min_value=1, value=50, step=1)

    if algo_selected == 'Algorithme genetique':
        pop_size = expander.number_input("Taille de la population", min_value=1, value=50, step=1)
        nbr_generations = expander.number_input("Nombre de générations", min_value=1, value=100, step=1)

    if col2.button("Lancer"):
        if algo_selected == 'Recuit simule':
            recuit = RecuitSimule(
                num_nodes=num_nodes,
                adjacency_matrix=adjacency_matrix,
                max_colors=max_colors,
                temperature_initiale=temperature_initiale,
                facteur=facteur,
                iterations=iterations,
                voisinages=voisinages
            )
            solution_recuit, _ = recuit.launch()
            solution_colors = [COLORS_LIST[color] for color in solution_recuit]

        if algo_selected == 'Algorithme genetique':
            genetique = Genetique(
                num_nodes=num_nodes,
                adjacency_matrix=adjacency_matrix,
                max_colors=max_colors,
                pop_size=pop_size,
                nbr_generations=nbr_generations
            )
            solution_genetique, _ = genetique.launch()
            solution_colors = [COLORS_LIST[color] for color in solution_genetique]

    # Mettre à jour la figure colorée dans le placeholder
    fig = geo_env.show_graph(colors=solution_colors, title=geojson_choice)
    col1.pyplot(fig)  # Met à jour la figure affichée