import random
import numpy as np

class RecuitSimule:
    def __init__(self, num_nodes, adjacency_matrix, max_colors, temperature_initiale, facteur, iterations, voisinages):
        self.num_nodes = num_nodes
        self.adjacency_matrix = adjacency_matrix
        self.max_colors = max_colors
        self.temperature_initiale = temperature_initiale
        self.facteur = facteur
        self.solution = [random.randint(0, max_colors - 1) for _ in range(num_nodes)]  # Solution initiale aléatoire
        self.cout_min_sol = self.calculer_conflits(self.solution)  # Coût initial
        self.min_sol = self.solution[:]
        self.iterations = iterations
        self.voisinages = voisinages

    def calculer_conflits(self, solution):
        """
        Calcule le nombre total de conflits dans la solution.
        """
        conflits = 0
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if self.adjacency_matrix[i][j] == 1 and solution[i] == solution[j]:  # Conflit
                    conflits += 1
        return conflits // 2  # Chaque conflit est compté deux fois (i -> j et j -> i)

    def voisinage(self, solution):
        """
        Génère une nouvelle solution voisine en changeant la couleur d'un sommet.
        """
        voisin = solution[:]
        sommet = random.randint(0, self.num_nodes - 1)
        nouvelle_couleur = random.choice([c for c in range(self.max_colors) if c != solution[sommet]])
        voisin[sommet] = nouvelle_couleur
        return voisin

    def launch(self):
        """
        Exécute l'algorithme de recuit simulé.
        """
        T = self.temperature_initiale
        cout_actuel = self.cout_min_sol
        historique = []

        for _ in range(self.iterations):
            T *= self.facteur
            for _ in range(self.voisinages):
                nouv_sol = self.voisinage(self.solution)
                cout_nouveau = self.calculer_conflits(nouv_sol)
                
                if cout_nouveau < cout_actuel:  # Meilleure solution trouvée
                    self.solution = nouv_sol
                    cout_actuel = cout_nouveau
                    if cout_nouveau < self.cout_min_sol:
                        self.cout_min_sol = cout_nouveau
                        self.min_sol = nouv_sol
                else:  # Probabilité d'accepter une solution pire
                    x = np.random.uniform()
                    if x < np.exp((cout_actuel - cout_nouveau) / T):
                        self.solution = nouv_sol
                        cout_actuel = cout_nouveau

            historique.append(cout_actuel)

        return self.min_sol, historique
