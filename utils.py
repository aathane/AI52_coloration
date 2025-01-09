import numpy as np
import csv
import os
import pandas as pd

def get_nb_conflicts(adjacency_matrix, solution, nb_nodes) -> int:
    """
    Computes the number of conflicts in the solution.

    Returns:
        conflicts (int) : the number of conflicts in the solution
    """
    conflicts = 0

    # Check conflicts for each edge in the adjacency matrix
    for i in range(nb_nodes):
        for j in range(i + 1, nb_nodes):  # Only check upper triangle (i < j)
            if adjacency_matrix[i][j] == 1 and solution[i] == solution[j]:
                conflicts += 1

    return conflicts

def save_results_to_csv(
        algorithm: str,
        map_choice: str,
        elapsed_time: float,
        nb_conflicts: int
    ) -> None:
    """
    Save the results of the graph coloring algorithm to a CSV file.
    
    This function appends the algorithm's results (algorithm name, map choice,
    computation time, and the number of conflicts) to a CSV file located at 
    'data/results.csv'. If the file does not exist, it creates the file and 
    writes the header before appending the results.

    Args:
        algorithm (str): The name of the algorithm used.
        map_choice (str): The map choice ('Regions' or 'Departments').
        elapsed_time (float): The time taken for the algorithm to complete, in seconds.
        nb_conflicts (int): The number of conflicts found during the solution process.
    
    Returns:
        None: This function does not return any value. It writes to a file.
    """

    # Check if the file already exists
    file_path = 'data/results.csv'
    file_exists = os.path.exists(file_path)
    
    # Open file in append mode
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # If the file doesn't exist, write the header
        if not file_exists:
            writer.writerow(['Algorithm', 'Map', 'Computation Time (s)', 'Number of Conflicts'])
        
        # Save results
        writer.writerow([algorithm, map_choice, elapsed_time, nb_conflicts])

def read_results_from_csv() -> pd.DataFrame:
    """
    Reads the results from the 'data/results.csv' file and returns them as a pandas DataFrame.
    
    If the file does not exist or is empty, an empty DataFrame is returned.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the algorithm results, with columns:
                      'Algorithm', 'Map', 'Computation Time (s)', 'Number of Conflicts'.
    """
    file_path = 'data/results.csv'

    # Check if the file exists
    if not os.path.exists(file_path):
        return pd.DataFrame(columns=['Algorithm', 'Map', 'Computation Time (s)', 'Number of Conflicts'])

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    return df