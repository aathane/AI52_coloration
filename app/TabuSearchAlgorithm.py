import random
import numpy as np

class TabuSearchAlgorithm:
    def __init__(
            self,
            nb_nodes: int,
            adjacency_matrix: np.ndarray,
            max_colors: int,
            max_iterations: int,
            tabu_tenure: int
        ):
        self.nb_nodes: int = nb_nodes
        self.adjacency_matrix: np.ndarray = adjacency_matrix
        self.max_colors: int = max_colors
        self.max_iterations: int = max_iterations
        self.tabu_tenure: int = tabu_tenure

        self.colors = [0 for _ in range(self.nb_nodes)]
        self.tabu_list = []
        self.best_solution = []
        self.best_conflicts = float('inf')
        

    def get_fitness(self) -> int:
        """
        Function that returns the fitness ie. the number of conflicts in the solution

        Returns:
            conflicts (int) the number of conflicts in the solution
        """
        conflicts = 0
        for i in range(self.nb_nodes):
            for j in range(self.nb_nodes):
                if self.adjacency_matrix[i][j] == 1 and self.colors[i] == self.colors[j]:  # Conflict
                    conflicts += 1
        return conflicts // 2  # Each conflict is counted twice (i -> j and j -> i)


    def update_tabu_list(self, move: tuple[int, int]) -> None:
        """
        Updates the tabu list by adding a new move and ensuring it respects the 
        maximum tabu tenure.

        Args:
            move (tuple[int, int]): A tuple representing the move to be added 
                                    to the tabu list.

        Returns:
            None
        """
        self.tabu_list.append(move)
        if len(self.tabu_list) > self.tabu_tenure:
            self.tabu_list.pop(0)

    def mat_tabou(self) -> np.ndarray:
        """
        Builds the Tabu matrix to determine the best moves.

        This function constructs a matrix where each element represents the 
        number of conflicts associated with assigning a specific color to a 
        node, considering both external conflicts with neighbors and internal 
        conflicts within the node itself.

        Returns:
            np.ndarray: A 2D array of shape (nb_nodes, max_colors), where each 
                        element represents the difference between the external 
                        conflicts (with neighbors) and the internal conflicts 
                        (within the node) for each possible color assignment.
        """
        tab = np.zeros((self.nb_nodes, self.max_colors))  # nb_nodes x nb_colors
        
        for i in range(self.nb_nodes):
            for j in range(self.max_colors):
                a = 0  # Conflicts caused by neighbors having color j
                b = 0  # Internal conflicts for node i with color j
                
                # Check the neighbors of node i and their color
                for k in range(self.nb_nodes):
                    if self.adjacency_matrix[i][k] == 1:  # There's an edge between i and k
                        if j == self.colors[k]:  # If k's color is j, it's a conflict
                            a += 1

                # Check internal conflicts within node i (if i has color j)
                for k in range(self.nb_nodes):
                    if self.adjacency_matrix[i][k] == 1 and self.colors[i] == self.colors[k]:
                        b += 1
                
                # Update the Tabu matrix
                tab[i][j] = a - b
        
        return tab

    def launch(self) -> list[int]:
        """
        Launches the tabu search algorithm for graph coloring. The algorithm 
        iteratively improves the coloring solution by exploring neighbors 
        and using a tabu list to avoid revisiting previous solutions.

        Returns:
            list[int]: The best coloring solution found, represented as a list where 
                        each element is the color assigned to the corresponding node.
        """
        self.best_solution = self.colors.copy()
        self.best_conflicts = self.get_fitness()

        iteration = 0
        while iteration < self.max_iterations and self.best_conflicts > 0:
            # Construire la matrice Tabou pour l'itération en cours
            tab = self.mat_tabou()

            # Trouver le nœud à changer en cherchant le minimum dans la matrice Tabou
            min_value = np.min(tab)
            nodes_to_change = np.argwhere(tab == min_value)

            # Sélectionner un nœud et une couleur parmi les candidats ayant la valeur minimale
            node_to_change, color_to_change = random.choice(nodes_to_change)

            # Si le nœud à changer est déjà dans la liste Tabu, on l'ignore
            if (node_to_change, color_to_change) not in self.tabu_list:
                self.colors[node_to_change] = color_to_change
                self.update_tabu_list((node_to_change, color_to_change))

                # Évaluer la solution actuelle
                current_conflicts = self.get_fitness()

                # Si la solution actuelle est meilleure, mettre à jour la meilleure solution
                if current_conflicts < self.best_conflicts:
                    self.best_solution = self.colors.copy()
                    self.best_conflicts = current_conflicts

            iteration += 1

        return self.best_solution