import numpy as np
import random as rd
from random import randint

class GeneticAlgorithm:
    def __init__(
            self,
            nb_nodes: int,
            adjacency_matrix: np.ndarray,
            max_colors: int,
            pop_size: int,
            nb_generations: int,
            mutation_rate : float,
            crossover_rate: float
        ):
        self.nb_nodes: int = nb_nodes
        self.adjacency_matrix: np.ndarray = adjacency_matrix
        self.max_colors: int = max_colors
        self.pop_size: int = pop_size
        self.nb_generations: int = nb_generations
        self.mutation_rate: float = mutation_rate
        self.crossover_rate: float = crossover_rate
        self.population: np.ndarray = self.generate_population()  # Random initial solution

    def generate_population(self) -> np.ndarray:
        """
        Generates an initial population where each node is assigned a random color.

        Args:
            None

        Returns:
            np.ndarray: A 2D array representing the population, where each row is 
                        a chromosome and each element is a randomly assigned color 
                        for a node.
        """
        population = np.random.randint(0, self.max_colors, size=(self.pop_size, self.nb_nodes))
        return population

    def get_fitness(self) -> np.ndarray:
        """
        Computes the fitness of each individual in the population, where the fitness 
        is defined as the number of conflicts in the solution.

        Returns:
            np.ndarray: An array where each element represents the fitness (number of conflicts) 
                        of the corresponding individual in the population.
        """
        conflicts = np.zeros(self.pop_size, dtype=int)

        # Iterate over each individual in the population
        for idx, solution in enumerate(self.population):
            # Check conflicts for each edge in the adjacency matrix
            for i in range(self.nb_nodes):
                for j in range(i + 1, self.nb_nodes):  # Only check upper triangle (i < j)
                    if self.adjacency_matrix[i][j] == 1 and solution[i] == solution[j]:
                        conflicts[idx] += 1

        return conflicts


    def selection(self, fitness: np.ndarray, nb_parents: int) -> np.ndarray:
        """
        Selects the best individuals as parents based on their fitness, 
        with a focus on minimizing fitness values.

        Args:
            fitness (np.ndarray): An array representing the fitness of each individual.
            nb_parents (int): The number of parents to be selected.

        Returns:
            np.ndarray: An array containing the selected parents.
        """
        parents = np.empty((nb_parents, self.nb_nodes), dtype=int)
        sorted_indices = np.argsort(fitness)  # Sort indices by increasing fitness
        for i in range(nb_parents):
            parents[i, :] = self.population[sorted_indices[i], :]
        return parents


    def crossover(self, parents: np.ndarray, nb_children: int) -> np.ndarray:
        """
        This function cross-references parents to give feedback on children

        Args:
            parents (np.ndarray) the parents chromosomes
            nb_children (int) the number of children that we want

        Returns:
            conflicts (int) the number of conflicts in the solution
        """
        children = np.empty((nb_children, self.nb_nodes), dtype=int)

        for i in range(nb_children):
            if rd.random() > self.crossover_rate:
                # If no crossover, choose a random parent
                children[i, :] = parents[i % parents.shape[0], :]
                continue

            parent1 = parents[i % parents.shape[0], :]
            parent2 = parents[(i + 1) % parents.shape[0], :]
            point_crossover = randint(0, self.nb_nodes - 1)
            children[i, :point_crossover] = parent1[:point_crossover]
            children[i, point_crossover:] = parent2[point_crossover:]

        return children

    def mutation(self, child: list[int]) -> list[int]:
        """
        Introduces random mutations to diversify the population.

        Args:
            child (np.ndarray): The chromosome representing a child solution.

        Returns:
            np.ndarray: A mutated version of the input child chromosome.
        """
        mutants: list[int] = child.copy()

        for i in range(mutants.shape[0]):
            if rd.random() < self.mutation_rate:
                node_to_mutate = randint(0, self.nb_nodes - 1)
                mutants[i, node_to_mutate] = randint(0, self.max_colors - 1)

        return mutants

    def launch(self) -> list[int]:
        """
        Launch the genetic algorithm to find a solution.

        Returns:
            list[int]: The solution found, or the solution with fitness 0 if it is encountered.
        """
        nb_parents = self.pop_size // 2
        nb_children = self.pop_size - nb_parents

        for _ in range(self.nb_generations):
            fitness = self.get_fitness()

            # Check if a solution with fitness 0 is found
            if 0 in fitness:
                best_index = np.argmin(fitness)
                return self.population[best_index].tolist()

            parents = self.selection(fitness, nb_parents)
            children = self.crossover(parents, nb_children)
            mutants = self.mutation(children)
            self.population[:nb_parents, :] = parents
            self.population[nb_parents:, :] = mutants

        # Finding the best solution after all generations
        fitness_final = self.get_fitness()
        best_index = np.argmin(fitness_final)
        best_solution = self.population[best_index]

        return best_solution.tolist()