# -*- coding: utf-8 -*-
"""
Created on Sat DEC 07 14:43:00 2024
Sujet  :  Coloration de graphes appliquée à la France
@author: ATHANE Augustin - VERNADE Mathias - MAURER Gilles - MEIRINHO Hugo
"""

# Import libs
from matplotlib import pyplot as plt
import pandas as pd
import streamlit as st
from geo_environment import GeoEnv
import time

# Import algorithms
from app.SimulatedAnnealingAlgorithm import SimulatedAnnealingAlgorithm
from app.GeneticAlgorithm import GeneticAlgorithm
from app.PSOAlgorithm import PSOAlgorithm
from app.TabuSearchAlgorithm import TabuSearchAlgorithm
from app.AntColonyAlgorithm import AntColonyAlgorithm
from utils import get_nb_conflicts, read_results_from_csv, save_results_to_csv

# Constants
COLORS_LIST = [
    "#FF0000",  # Red
    "#0000FF",  # Blue
    "#FFFF00",  # Yellow
    "#00FF00",  # Green
    "#FF00FF",  # Magenta
    "#00FFFF",  # Cyan
    "#800000",  # Brown
    "#808000",  # Olive
    "#008080",  # Turquoise
    "#800080"   # Purple
]

NB_ITERATIONS = 500

NB_COULEURS = 4

DO_SAVE_RESULT = False

# Streamlit UI
# Title
st.markdown("""<h1 style='text-align: center; color: black;'>Coloration de Graphes : Régions Métropolitaines de France</h1><hr style='border: 2px solid blue;'>""", unsafe_allow_html=True)

# Navigation bar
add_sidebar = st.sidebar.selectbox('Choisir la page', ('Algorithmes', 'Résultats'))

# Algorithm page
if add_sidebar == 'Algorithmes':
    elapsed_time = None
    nb_conflicts = None
    st.subheader('Test et démonstration des algorithmes')
    geojson_choice = st.selectbox('Choisir une carte', ('Régions', 'Départements'))

    # Reset colors
    solution_colors = None

    # Séparer en 2 colonnes :
    col1, col2 = st.columns(2)

    # Initialiser l'environnement et la figure sans couleur
    geo_env = GeoEnv(geojson_choice)
    adjacency_matrix, region_names = geo_env.adjacency_matrix()
    nb_nodes = len(region_names)

    # Colonne 2 : Sélection de l'algorithme
    algo_selected = col2.selectbox('Choisir un Algorithme', ('Recuit simulé', 'Algorithme génétique', 'ACO', 'Recherche tabou', 'PSO'))
    
    expander = col2.expander("Plus de paramètres")

    if algo_selected == 'Recuit simulé':
        temperature_initiale = expander.number_input("Température initiale", min_value=1, value=1000, step=1)
        facteur = expander.number_input("Facteur de réduction", min_value=0.01, max_value=1.0, value=0.95, step=0.01)

    if algo_selected == 'Algorithme génétique':
        pop_size = expander.number_input("Taille de la population", min_value=1, value=50, step=1)
        mutation_rate = expander.number_input("Taux de mutation", min_value=0.1, max_value=1.0, value=0.5, step=0.1)
        crossover_rate = expander.number_input("Taux de croisement", min_value=0.1, max_value=1.0, value=0.8, step=0.1)

    if algo_selected == 'ACO':
        evaporation_rate = expander.number_input("Taux d'évaporation", min_value=0.01, value=0.5, step=0.01, max_value=1.0)
        alpha = expander.number_input("Paramètre alpha", min_value=0.1, value=1.0, step=0.1, max_value=10.0)
        beta = expander.number_input("Paramètre beta", min_value=0.1, value=3.0, step=0.1, max_value=10.0)
        pheromone_quantity = expander.number_input("Quantité de phéromone", min_value=0.1, value=10.0, step=1.0, max_value=100.0)

    if algo_selected == 'Recherche tabou':
        tabu_tenure = expander.number_input("Longueur de la liste tabou", min_value=1, value=5, step=1)

    if algo_selected == 'PSO':
        swarm_size = expander.number_input("Nombre de particules", min_value=1, value=30, step=1)
        inertia_weight = expander.number_input("Poids d'inertie", min_value=0.1, value=0.7, step=0.1, max_value=1.0)
        cognitive_weight = expander.number_input("Poids cognitif", min_value=0.1, value=1.5, step=0.1)
        social_weight = expander.number_input("Poids social", min_value=0.1, value=1.5, step=0.1)


    if col2.button("Lancer"):
        if algo_selected == 'Recuit simulé':
            algorithm = SimulatedAnnealingAlgorithm(
                nb_nodes=nb_nodes,
                adjacency_matrix=adjacency_matrix,
                max_colors=NB_COULEURS,
                initial_temperature=temperature_initiale,
                factor=facteur,
                iterations=NB_ITERATIONS,
            )

        if algo_selected == 'Algorithme génétique':
            algorithm = GeneticAlgorithm(
                nb_nodes=nb_nodes,
                adjacency_matrix=adjacency_matrix,
                max_colors=NB_COULEURS,
                pop_size=pop_size,
                nb_generations=NB_ITERATIONS,
                mutation_rate = mutation_rate,
                crossover_rate = crossover_rate
            )

        if algo_selected == 'ACO':
            algorithm = AntColonyAlgorithm(
                adjacency_matrix=adjacency_matrix,
                max_colors=NB_COULEURS,
                evaporation_rate=evaporation_rate,
                alpha=alpha,
                beta=beta,
                nb_iterations=100,
                pheromone_quantity=pheromone_quantity
            )

        if algo_selected == 'Recherche tabou':
            algorithm = TabuSearchAlgorithm(
                nb_nodes=nb_nodes,
                adjacency_matrix=adjacency_matrix,
                max_colors=NB_COULEURS,
                max_iterations=NB_ITERATIONS,
                tabu_tenure=tabu_tenure
            )

        if algo_selected == 'PSO':
            algorithm = PSOAlgorithm(
                nb_nodes=nb_nodes,
                adjacency_matrix=adjacency_matrix,
                max_colors=NB_COULEURS,
                max_iterations=100,
                swarm_size=swarm_size,
                inertia_weight=inertia_weight,
                cognitive_weight=cognitive_weight,
                social_weight=social_weight
            )
        

        # Démarrer le chronomètre
        start_time = time.time()
        
        solution = algorithm.launch()

        # Calculer le temps écoulé
        elapsed_time = time.time() - start_time

        solution_colors = [COLORS_LIST[color] for color in solution]
        nb_conflicts = get_nb_conflicts(adjacency_matrix, solution, nb_nodes)

    # Mettre à jour la figure colorée dans le placeholder
    fig = geo_env.show_graph(colors=solution_colors, title=geojson_choice)
    col1.pyplot(fig)  # Met à jour la figure affichée

    if (DO_SAVE_RESULT and (elapsed_time != None) and (nb_conflicts != None)):
        # Add the computation time and the number of conflicts at the bottom
        col3, col4 = st.columns(2)

        # Column for computation time
        col3.markdown(f"**Temps de calcul**: {elapsed_time:.2f} secondes")

        # Column for number of conflicts
        col4.markdown(f"**Nombre de conflits**: {nb_conflicts}")

        save_results_to_csv(algo_selected, geojson_choice, elapsed_time, nb_conflicts)
        
# Page Résultats
if add_sidebar == 'Résultats':
    st.subheader('Résultats des Algorithmes')

    # Charger les résultats depuis le CSV
    results: pd.DataFrame = read_results_from_csv()

    if results.empty:
        st.write("Aucun résultat disponible.")
    else:       
        # Séparer les résultats en fonction de la "Map"
        maps = results['Map'].unique()
        
        for map_name in maps:
            st.subheader(f"Résultats pour la Map: {map_name}")
            
            # Filtrer les résultats pour cette map
            filtered_results = results[results['Map'] == map_name]
            
            # Créer les graphiques pour chaque map
            fig, ax = plt.subplots(1, 2, figsize=(14, 6))

            # Graphique du temps de calcul
            ax[0].bar(filtered_results['Algorithm'], filtered_results['Computation Time (s)'])
            ax[0].set_title(f"Temps de Calcul par Algorithme ({map_name})")
            ax[0].set_ylabel("Temps (secondes)")
            ax[0].set_xticklabels(filtered_results['Algorithm'].unique(), rotation=45)

            # Graphique du nombre de conflits
            ax[1].bar(filtered_results['Algorithm'], filtered_results['Number of Conflicts'])
            ax[1].set_title(f"Nombre de Conflits par Algorithme ({map_name})")
            ax[1].set_ylabel("Nombre de Conflits")
            ax[1].set_xticklabels(filtered_results['Algorithm'].unique(), rotation=45)

            st.pyplot(fig)

        # Afficher les résultats sous forme de tableau pour cette map
        st.dataframe(filtered_results)
