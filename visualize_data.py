import numpy as np
from collections import defaultdict
import os
import matplotlib.pyplot as plt


# Updated function to read and compute mean execution times for each node count
def read_and_aggregate_execution_times(file_path, node_counts):
    """
    Reads the execution time data from a file and computes the mean execution times for each node count.

    Parameters:
        file_path (str): The path to the file containing the data.
        node_counts (list): A list of node counts corresponding to each data point.

    Returns:
        dict: A dictionary with node counts as keys and mean execution times as values.
    """
    execution_times = []
    with open(file_path, 'r') as f:
        for line in f:
            try:
                _, execution_time = line.strip().split(',')
                execution_times.append(float(execution_time))
            except ValueError:
                print(f"Skipping malformed line: {line.strip()}")

    if len(execution_times) != len(node_counts):
        raise ValueError(f"Mismatch between execution times ({len(execution_times)}) and node counts ({len(node_counts)}).")

    # Aggregate execution times by node count
    aggregated = defaultdict(list)
    for node, time in zip(node_counts, execution_times):
        aggregated[node].append(time)

    # Compute the mean for each node count
    return {node: np.mean(times) for node, times in aggregated.items()}


# Function to save plots
def save_plot_with_check(title, fig):
    """
    Saves the plot to a file, ensuring the 'tables' directory exists.

    Parameters:
        title (str): The title of the plot for the filename.
        fig (matplotlib.figure.Figure): The plot figure.
    """
    if not os.path.exists("tables"):
        os.makedirs("tables")
    fig.savefig(f"tables/{title}_execution_time_comparison.png")
    plt.show()


import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

def plot_execution_times(file_paths, node_counts):
    """
    Plots the mean execution times for different algorithms (excluding brute force).

    Parameters:
        file_paths (dict): A dictionary with algorithm names as keys and file paths as values.
        node_counts (list): A list of node counts corresponding to each data point.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))

    for algorithm, file_path in file_paths.items():
        if algorithm == "brute_force_coloring":
            continue  # Skip brute force algorithm

        try:
            # Read and aggregate execution times
            mean_execution_times = read_and_aggregate_execution_times(file_path, node_counts)

            # Extract sorted node counts and corresponding mean execution times
            sorted_nodes = sorted(mean_execution_times.keys())
            sorted_times = [mean_execution_times[node] for node in sorted_nodes]

            # Plot the data for the current algorithm
            plt.plot(sorted_nodes, sorted_times, label=algorithm, marker='o')
        except Exception as e:
            print(f"Error processing {algorithm}: {e}")

    # Add labels, title, and legend
    plt.xlabel("Node Counts")
    plt.ylabel("Mean Execution Time (seconds)")
    plt.title("Execution Time vs. Node Counts for Different Algorithms (Excluding Brute Force)")
    plt.legend()
    plt.grid(True)

    # Save and show the plot
    fig = plt.gcf()
    save_plot_with_check("execution_time_comparison_no_bruteforce", fig)

# Call the function to plot execution times
# Example usage: file paths for algorithms
file_paths = {
    "dsatur": "statistics/dsatur_avg_colors_and_time.csv",
    "greedy_with_degree": "statistics/greedy_with_degree_avg_colors_and_time.csv",
    "greedy_basic": "statistics/greedy_basic_avg_colors_and_time.csv",
    "brute_force_coloring": "statistics/brute_force_coloring_avg_colors_and_time.csv"
}

# Node counts for the 20 tests
node_counts = [11, 12, 13, 14, 11, 12, 13, 14, 11, 12, 13, 14, 11, 12, 13, 14, 11, 12, 13, 14]
# Call the function to plot execution times
plot_execution_times(file_paths, node_counts)

# Call the plotting function
