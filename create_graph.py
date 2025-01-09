# Import libs
import streamlit as st
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from geo_environment import GeoEnv

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
    "#ced4da"   # Purple
]

def transition(solution: list[int]) -> list[int]:
    """
    Fait passer de la configuration de la solution manuelle a la configuration de la solution voulue par la fonction
    """
    indices = [2, 5, 3, 4, 1, 0, 7, 8, 9, 11, 6, 10]
    return [solution[i] for i in indices]



def main(solution: list[int]):
    # Initialiser l'environnement et la figure sans couleur
    geo_env = GeoEnv('Régions')

    # Conversion vers le bon graph et pour les couleurs

    solution_colors = [COLORS_LIST[color] for color in transition(solution)]

    # Mettre à jour la figure colorée dans le placeholder
    fig = geo_env.show_graph(colors=solution_colors, title='Régions')

    # Sauvegarder la figure en tant qu'image
    fig.savefig("output_graph.png")

if __name__ == "__main__":
    solution: list[int] = [1, 2, 0, 3, 3, 1, 3, 2, 0, 0, 2, 0]
    main(solution)