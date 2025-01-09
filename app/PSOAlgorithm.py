import random
import numpy as np

class PSOAlgorithm:
    def __init__(
            self,
            nb_nodes: int,
            adjacency_matrix: np.ndarray,
            max_colors: int,
            max_iterations: int,
            swarm_size: int,
            inertia_weight: float,
            cognitive_weight: float,
            social_weight: float
        ):

        self.nb_nodes: int = nb_nodes
        self.adjacency_matrix: np.ndarray  = adjacency_matrix
        self.max_colors: int = max_colors
        self.max_iterations: int = max_iterations
        self.swarm_size: int = swarm_size
        self.inertia_weight: float = inertia_weight
        self.cognitive_weight: float = cognitive_weight
        self.social_weight: float = social_weight
        
        self.particles = []
        self.best_solution = []
        self.best_conflicts: float = float('inf')

    def initialize_particles(self) -> None:
        """Initializes the particles with random colorations.

        This method creates particles for the swarm, each with a random color 
        configuration representing its position. It also initializes their velocity 
        and sets their best position and corresponding conflict count.
        """
        self.particles = []
        for _ in range(self.swarm_size):
            colors = [random.randint(0, self.max_colors - 1) for _ in range(self.nb_nodes)]
            self.particles.append({
                'position': colors,         # Position de la particule (coloration)
                'velocity': [0] * self.nb_nodes,  # Vitesse de la particule (changement dans la coloration)
                'best_position': colors,    # Meilleure position de la particule
                'best_conflicts': self.get_fitness(colors)  # Conflits pour cette position
            })

    def get_fitness(self, colors: list[int]) -> int:
        """
        Function that returns the fitness ie. the number of conflicts in the solution

        Args:
            colors (list[int])

        Returns:
            conflicts (int) the number of conflicts in the solution
        """
        conflicts = 0
        for i in range(self.nb_nodes):
            for j in range(self.nb_nodes):
                if self.adjacency_matrix[i][j] == 1 and colors[i] == colors[j]:  # Conflict
                    conflicts += 1
        return conflicts // 2  # Each conflict is counted twice (i -> j and j -> i)
    
    def update_velocity(self, particle: dict) -> None:
        """Updates the velocity of the particle.

        This method calculates the new velocity of a particle based on the inertia, 
        cognitive, and social components. The cognitive component drives the particle 
        toward its personal best position, while the social component drives it toward 
        the global best solution. The velocity is bounded between -1 and 1.

        Args:
            particle (dict): A dictionary representing the particle, containing 'position', 
                            'velocity', 'best_position', and 'best_conflicts'.
        """
        for i in range(self.nb_nodes):
            r1 = random.random()  # Random factor for cognitive component
            r2 = random.random()  # Random factor for social component

            cognitive_component = self.cognitive_weight * r1 * (particle['best_position'][i] - particle['position'][i])
            social_component = self.social_weight * r2 * (self.best_solution[i] - particle['position'][i])
            inertia_component = self.inertia_weight * particle['velocity'][i]

            particle['velocity'][i] = inertia_component + cognitive_component + social_component

            # Limit velocity (to prevent too large jumps in the solution space)
            particle['velocity'][i] = max(-1, min(1, particle['velocity'][i]))


    def update_position(self, particle: dict) -> None:
        """Updates the position of the particle (the colors of the nodes).

        This method adjusts the particle's position based on its velocity. The new position 
        is computed as the current position plus the velocity, modulo the maximum number of colors.

        Args:
            particle (dict): A dictionary representing the particle, containing 'position' and 'velocity'.
        """
        for i in range(self.nb_nodes):
            particle['position'][i] = (particle['position'][i] + int(particle['velocity'][i])) % self.max_colors


    def update_personal_best(self, particle: dict) -> None:
        """Updates the particle's personal best position if necessary.

        This method compares the current conflicts of the particle's position with its personal 
        best conflicts. If the current position has fewer conflicts, the personal best is updated.

        Args:
            particle (dict): A dictionary representing the particle, containing 'position', 
                            'best_position', and 'best_conflicts'.
        """
        current_conflicts = self.get_fitness(particle['position'])
        if current_conflicts < particle['best_conflicts']:
            particle['best_position'] = particle['position']
            particle['best_conflicts'] = current_conflicts


    def update_global_best(self) -> None:
        """Updates the global best solution.

        This method iterates over all particles and updates the global best solution 
        if any particle has a better (lower conflict) solution.

        Updates the global best solution and conflict count if necessary.
        """
        for particle in self.particles:
            if particle['best_conflicts'] < self.best_conflicts:
                self.best_solution = particle['best_position']
                self.best_conflicts = particle['best_conflicts']

    def launch(self) -> list[int]:
        """
        Launches the PSO search algorithm for graph coloring.

        Returns:
            list[int]: The best coloring solution found, represented as a list where 
                        each element is the color assigned to the corresponding node.
        """
        self.initialize_particles()
        self.best_solution = self.particles[0]['position']
        self.best_conflicts = self.particles[0]['best_conflicts']

        iteration = 0
        while iteration < self.max_iterations and self.best_conflicts > 0:
            for particle in self.particles:
                # Mettre à jour la vitesse et la position de chaque particule
                self.update_velocity(particle)
                self.update_position(particle)
                # Mettre à jour la meilleure position de la particule
                self.update_personal_best(particle)

            # Mettre à jour la meilleure solution globale
            self.update_global_best()

            iteration += 1

        return self.best_solution
