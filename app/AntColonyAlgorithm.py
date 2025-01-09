import numpy as np

class AntColonyAlgorithm:    
    def __init__(
        self,
        adjacency_matrix: np.ndarray,
        max_colors: int,
        evaporation_rate: float,
        alpha: float,
        beta: float,
        nb_iterations: int,
        pheromone_quantity: float
    ):
        self.adjacency_matrix: np.ndarray = adjacency_matrix
        self.nb_nodes: int = len(adjacency_matrix)
        self.max_colors: int = max_colors
        self.evaporation_rate: float = evaporation_rate
        self.alpha: float = alpha
        self.beta: float = beta
        self.nb_ants: int = 5
        self.nb_iterations: int = nb_iterations
        self.pheromone_quantity: float = pheromone_quantity

    def get_probability(
            self,
            pheromone_matrix: np.ndarray,
            current_node: int,
            solution: list[int]
        ) -> np.ndarray:
        """
        Calculates the probabilities of choosing a color for a given node.

        Args:
            pheromone_matrix (np.ndarray): The matrix of pheromone levels for each node-color pair.
            current_node (int): The node for which the color choice probability is calculated.
            solution (List[int]): The current color assignment for all nodes.

        Returns:
            np.ndarray: A probability distribution over the available colors for the current node.
        """
        pheromone_component = pheromone_matrix[current_node] ** self.alpha
        conflict_component = np.zeros(self.max_colors)

        # Penalize colors that would cause conflicts
        for color in range(self.max_colors):
            conflict_component[color] = 1 / (1 + sum(
                1 for neighbor in range(self.nb_nodes)
                if self.adjacency_matrix[current_node][neighbor] == 1 and solution[neighbor] == color
            ))

        conflict_component **= self.beta
        probability = pheromone_component * conflict_component
        probability /= np.sum(probability)
        return probability

    def get_fitness(self, solution: list[int]) -> int:
        """
        Calculates the fitness of a given solution.

        The fitness is defined as the number of conflicts, where two adjacent nodes 
        are assigned the same color.

        Args:
            solution (List[int]): A list representing the color assignment for each node.

        Returns:
            int: The number of conflicts in the solution.
        """
        conflicts = 0
        for i in range(self.nb_nodes):
            for j in range(i + 1, self.nb_nodes):
                if self.adjacency_matrix[i][j] == 1 and solution[i] == solution[j]:
                    conflicts += 1
        return conflicts


    def launch(self) -> list[int]:
        """
        Runs the Ant Colony Optimization algorithm to solve the graph coloring problem.

        The algorithm iteratively updates pheromones and constructs solutions, aiming to minimize
        the number of conflicts (adjacent nodes sharing the same color).

        Returns:
            List[int]: The best color assignment solution found by the algorithm.
        """
        pheromone_matrix = np.ones((self.nb_nodes, self.max_colors))
        best_solution: list[int] = None
        best_conflicts = float('inf')

        for i in range(self.nb_iterations):
            print(i)
            solutions = []
            conflicts = []

            # Each ant constructs a solution
            for ant in range(self.nb_ants):
                solution = [-1] * self.nb_nodes
                for node in range(self.nb_nodes):
                    probabilities = self.get_probability(pheromone_matrix, node, solution)
                    solution[node] = np.random.choice(range(self.max_colors), p=probabilities)

                solutions.append(solution)
                conflicts.append(self.get_fitness(solution))

            # Update the best solution
            min_conflicts = min(conflicts)
            if min_conflicts < best_conflicts:
                best_conflicts = min_conflicts
                best_solution = solutions[conflicts.index(min_conflicts)]

            # Update pheromones
            pheromone_matrix *= (1 - self.evaporation_rate)
            for solution, conflict in zip(solutions, conflicts):
                pheromone_increase = self.pheromone_quantity / (1 + conflict)
                for node, color in enumerate(solution):
                    pheromone_matrix[node][color] += pheromone_increase

            # Stop if a perfect solution is found
            if best_conflicts == 0:
                break

        return best_solution