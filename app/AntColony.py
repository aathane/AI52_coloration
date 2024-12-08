import numpy as np

class AntColony:    
    def __init__(self, adjacency_matrix, max_colors, evaporation_rate, alpha, beta, nb_ants, nb_iterations, pheromone_quantity):
        self.adjacency_matrix = adjacency_matrix
        self.nb_nodes = len(adjacency_matrix)
        self.max_colors = max_colors
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.nb_ants = nb_ants
        self.nb_iterations = nb_iterations
        self.pheromone_quantity = pheromone_quantity

    def calculate_conflicts(self, solution):
        """
        Calcule le nombre de conflits pour une solution donnée.
        """
        conflicts = 0
        for i in range(self.nb_nodes):
            for j in range(i + 1, self.nb_nodes):
                if self.adjacency_matrix[i][j] == 1 and solution[i] == solution[j]:
                    conflicts += 1
        return conflicts

    def get_probability(self, pheromone_matrix, current_node, solution):
        """
        Calcule les probabilités de choisir une couleur pour un nœud donné.
        """
        pheromone_component = pheromone_matrix[current_node] ** self.alpha
        conflict_component = np.zeros(self.max_colors)

        # Penaliser les couleurs qui causeraient des conflits
        for color in range(self.max_colors):
            conflict_component[color] = 1 / (1 + sum(
                1 for neighbor in range(self.nb_nodes)
                if self.adjacency_matrix[current_node][neighbor] == 1 and solution[neighbor] == color
            ))

        conflict_component **= self.beta
        probability = pheromone_component * conflict_component
        probability /= np.sum(probability)
        return probability

    def launch(self):
        """
        Lance l'algorithme de colonie de fourmis pour résoudre la coloration de graphe.
        """
        pheromone_matrix = np.ones((self.nb_nodes, self.max_colors))
        best_solution = None
        best_conflicts = float('inf')
        history = []

        for _ in range(self.nb_iterations):
            solutions = []
            conflicts = []

            # Chaque fourmi construit une solution
            for ant in range(self.nb_ants):
                solution = [-1] * self.nb_nodes
                for node in range(self.nb_nodes):
                    probabilities = self.get_probability(pheromone_matrix, node, solution)
                    solution[node] = np.random.choice(range(self.max_colors), p=probabilities)

                solutions.append(solution)
                conflicts.append(self.calculate_conflicts(solution))

            # Mettre à jour la meilleure solution
            min_conflicts = min(conflicts)
            if min_conflicts < best_conflicts:
                best_conflicts = min_conflicts
                best_solution = solutions[conflicts.index(min_conflicts)]

            # Mise à jour des phéromones
            pheromone_matrix *= (1 - self.evaporation_rate)
            for solution, conflict in zip(solutions, conflicts):
                pheromone_increase = self.pheromone_quantity / (1 + conflict)
                for node, color in enumerate(solution):
                    pheromone_matrix[node][color] += pheromone_increase

            history.append(best_conflicts)

            # Arrêt si solution parfaite
            if best_conflicts == 0:
                break

        return best_solution, history
