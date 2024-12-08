import numpy as np
import random as rd
from random import randint

class Genetique:
    def __init__(self, num_nodes, adjacency_matrix, max_colors, pop_size=50, nbr_generations=500):
        self.num_nodes = num_nodes
        self.adjacency_matrix = adjacency_matrix
        self.max_colors = max_colors
        self.pop_size = pop_size
        self.nbr_generations = nbr_generations
        self.population = self.generate_population()

    def generate_population(self):
        """
        Génère une population initiale où chaque sommet reçoit une couleur aléatoire.
        """
        population = np.random.randint(0, self.max_colors, size=(self.pop_size, self.num_nodes))
        return population

    def cal_fitness(self):
        """
        Calcule la fitness de chaque individu dans la population.
        La fitness est basée sur le nombre de conflits dans la solution.
        Moins de conflits = meilleure fitness.
        """
        fitness = np.zeros(self.population.shape[0])
        for i in range(self.population.shape[0]):
            conflicts = 0
            for node in range(self.num_nodes):
                for neighbor in range(self.num_nodes):
                    if self.adjacency_matrix[node, neighbor] == 1:  # Si les deux sommets sont connectés
                        if self.population[i, node] == self.population[i, neighbor]:  # Conflit
                            conflicts += 1
            fitness[i] = 1 / (1 + conflicts)  # Inverse du nombre de conflits pour que moins de conflits = meilleure fitness
        return fitness

    def selection(self, fitness, nbr_parents):
        """
        Sélectionne les meilleurs individus comme parents en fonction de leur fitness.
        """
        parents = np.empty((nbr_parents, self.num_nodes), dtype=int)
        sorted_indices = np.argsort(fitness)[::-1]  # Tri par fitness décroissante
        for i in range(nbr_parents):
            parents[i, :] = self.population[sorted_indices[i], :]
        return parents

    def croisement(self, parents, nbr_enfants):
        """
        Produit des enfants en combinant des solutions parentales.
        """
        enfants = np.empty((nbr_enfants, self.num_nodes), dtype=int)
        taux_de_croisement = 0.8

        for i in range(nbr_enfants):
            if rd.random() > taux_de_croisement:
                # Si aucun croisement, choisir un parent au hasard
                enfants[i, :] = parents[i % parents.shape[0], :]
                continue

            parent1 = parents[i % parents.shape[0], :]
            parent2 = parents[(i + 1) % parents.shape[0], :]
            point_croisement = randint(0, self.num_nodes - 1)
            enfants[i, :point_croisement] = parent1[:point_croisement]
            enfants[i, point_croisement:] = parent2[point_croisement:]

        return enfants

    def mutation(self, enfants):
        """
        Introduit des mutations aléatoires pour diversifier la population.
        """
        mutants = enfants.copy()
        taux_mutation = 0.2

        for i in range(mutants.shape[0]):
            if rd.random() < taux_mutation:
                node_to_mutate = randint(0, self.num_nodes - 1)
                mutants[i, node_to_mutate] = randint(0, self.max_colors - 1)

        return mutants

    def launch(self):
        """
        Lance l'algorithme génétique pour résoudre le problème.
        """
        historique_fitness = []
        nbr_parents = self.pop_size // 2
        nbr_enfants = self.pop_size - nbr_parents

        for generation in range(self.nbr_generations):
            fitness = self.cal_fitness()
            historique_fitness.append(np.max(fitness))
            parents = self.selection(fitness, nbr_parents)
            enfants = self.croisement(parents, nbr_enfants)
            mutants = self.mutation(enfants)
            self.population[:nbr_parents, :] = parents
            self.population[nbr_parents:, :] = mutants

        # Trouver la meilleure solution
        fitness_final = self.cal_fitness()
        best_index = np.argmax(fitness_final)
        best_solution = self.population[best_index]

        return best_solution.tolist(), historique_fitness