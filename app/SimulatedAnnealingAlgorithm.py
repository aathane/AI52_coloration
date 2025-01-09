import random
import numpy as np

class SimulatedAnnealingAlgorithm:
    def __init__(
            self,
            nb_nodes: int,
            adjacency_matrix: np.ndarray,
            max_colors: int,
            initial_temperature: float,
            factor: float,
            iterations: int,
        ):
        self.nb_nodes: int = nb_nodes
        self.adjacency_matrix: np.ndarray = adjacency_matrix
        self.max_colors: int = max_colors
        self.initial_temperature: float = initial_temperature
        self.factor: float = factor
        self.solution: list[int] = [random.randint(0, max_colors - 1) for _ in range(nb_nodes)]  # Random initial solution
        self.min_fitness: int = self.get_fitness(self.solution)  # Initial cost
        self.min_sol: list[int] = self.solution[:]
        self.iterations: int = iterations

    def get_fitness(self, solution: list[int]) -> int:
        """
        Function that returns the fitness ie. the number of conflicts in the solution

        Args:
            solution (list[int])

        Returns:
            conflicts (int) the number of conflicts in the solution
        """
        conflicts = 0
        for i in range(self.nb_nodes):
            for j in range(self.nb_nodes):
                if self.adjacency_matrix[i][j] == 1 and solution[i] == solution[j]:  # Conflict
                    conflicts += 1
        return conflicts // 2  # Each conflict is counted twice (i -> j and j -> i)

    def neighborhood(self, solution: list[int]) -> list[int]:
        """
        Generates the adjacency matrix for the regions of France.

        Args:
            solution (list[int])

        Returns:
            conflicts (int) the number of conflicts in the solution
        """
        voisin = solution[:]
        sommet = random.randint(0, self.nb_nodes - 1)
        nouvelle_couleur = random.choice([c for c in range(self.max_colors) if c != solution[sommet]])
        voisin[sommet] = nouvelle_couleur
        return voisin

    def launch(self) -> list[int]:
        """
        Launch the simulated annealing algorithm to find a solution.

        Returns:
            self.min_sol (list[int]) the solution with the minimum fitness found
        """
        # Initialization
        T = self.initial_temperature
        current_fitness = self.min_fitness
        for _ in range(self.iterations):
            # Update temperature
            T *= self.factor

            # randomly select a neighbor of s uniformly
            neighbor_sol = self.neighborhood(self.solution) 
            neighbor_fitness = self.get_fitness(neighbor_sol)  
            
            if neighbor_fitness < current_fitness:
                self.solution = neighbor_sol
                current_fitness = neighbor_fitness
                # Update the best solution
                if neighbor_fitness < self.min_fitness:
                    self.min_fitness = neighbor_fitness
                    self.min_sol = neighbor_sol
            else:  # Accept worse solution with a certain probability
                prob = np.random.uniform()
                if prob < np.exp((current_fitness - neighbor_fitness) / T):
                    self.solution = neighbor_sol
                    current_fitness = neighbor_fitness
            
            # if there is no more conflict, then return the solution
            if self.min_fitness == 0:
                break

        return self.min_sol  # Return the best solution found