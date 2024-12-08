# -*- coding: utf-8 -*-
"""
Created on Sun DEC 08 12:06:00 2024
Sujet  :  Coloration de graphes appliquée à la France
@author: ATHANE Augustin - VERNADE Mathias - MAURER Gilles - MEIRINHO Hugo
"""

# Import libs
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

# Constants
BORDER_COLOR = "#FFFFFF"
NO_COLOR = "#808080"

METROPOLITAN_REGIONS = [
    "Auvergne-Rhône-Alpes", "Bourgogne-Franche-Comté", "Bretagne", "Centre-Val de Loire", "Grand Est", "Hauts-de-France", "Île-de-France", "Normandie",
    "Nouvelle-Aquitaine", "Occitanie", "Pays de la Loire", "Provence-Alpes-Côte d'Azur"
]
DEPARTEMENTS_INTERDITES = ["Corse-du-Sud", "Haute-Corse"]

# Definition of the class
class Region:
    def __init__(self, name="", color=NO_COLOR, neighbors=[]):
        self.color = color
        self.name = name
        self.neighbors = neighbors

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

class GeoEnv:
    def __init__(self, choice):
        if choice == "departements":
            geojson_path = "data/departements.geojson"

            self.gdf = gpd.read_file(geojson_path)

            self.gdf = self.gdf[~self.gdf['nom'].isin(DEPARTEMENTS_INTERDITES)]  # Exclure les departements interdits
        elif choice == "regions":
            geojson_path = "data/regions.geojson"

            self.gdf = gpd.read_file(geojson_path)

            # Filtrage des régions et gestion des erreurs si le GeoDataFrame est vide
            self.gdf = self.gdf[self.gdf['nom'].isin(METROPOLITAN_REGIONS)]
        
        else:
            return  # Arrêter l'exécution si le GeoDataFrame est vide
                
        
        # Vérification si le GeoDataFrame est vide
        if self.gdf.empty:
            print(f"Le fichier GeoJSON {geojson_path} est vide ou invalide.")
            return  # Arrêter l'exécution si le GeoDataFrame est vide
                
        
        # Vérification de la projection et transformation si nécessaire
        if self.gdf.crs is None or self.gdf.crs.to_string() != "EPSG:4326":
            print("Projection avant:", self.gdf.crs)
            self.gdf = self.gdf.to_crs(epsg=4326)  # Projection en latitude/longitude (EPSG:4326)
            print("Projection après:", self.gdf.crs)

        # Construction du graphe des voisins
        self.france_graph = {}
        for _, region in self.gdf.iterrows():
            region_name = region['nom']  # Nom de la région ou du département
            neighbors = self.gdf[self.gdf.geometry.touches(region.geometry)]['nom'].tolist()
            self.france_graph[region_name] = Region(region_name, NO_COLOR, neighbors)

    def adjacency_matrix(self):
        region_names = list(self.france_graph.keys())
        size = len(region_names)
        adj_matrix = np.zeros((size, size), dtype=int)
        for i, region in enumerate(region_names):
            for neighbor in self.france_graph[region].neighbors:
                if neighbor in region_names:
                    j = region_names.index(neighbor)
                    adj_matrix[i, j] = 1
                    adj_matrix[j, i] = 1
        return adj_matrix, region_names

    def show_graph(self, colors=None, title="Map"):
        if self.gdf.empty:
            print("Le GeoDataFrame est vide, impossible d'afficher la carte.")
            return
        
        if colors == None:
            colors=[NO_COLOR] * len(self.gdf)
        
        self.gdf['color'] = colors
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        
        # Affichage de la carte avec un aspect ajusté
        self.gdf.plot(ax=ax, color=self.gdf['color'], edgecolor=BORDER_COLOR)
        ax.set_title(title, fontsize=16)
        ax.axis('off')

        # Ajustement dynamique de l'aspect pour éviter l'erreur
        ax.set_aspect('auto')  # Nous utilisons 'auto' pour un ajustement dynamique en fonction du contenu

        return fig