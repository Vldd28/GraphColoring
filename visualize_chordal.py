import matplotlib.pyplot as plt
import numpy as np
import os
from collections import defaultdict

# Function to read the average colors used and execution time data
def read_algorithm_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            avg_colors_used, execution_time = line.strip().split(',')
            data.append((float(avg_colors_used), float(execution_time)))
    return data

# Function to ensure the 'tables' directory exists and save the plot
def save_plot_with_check(algorithm, fig):
    if not os.path.exists("chordal_tables"):
        os.makedirs("chordal_tables")
    fig.savefig(f"chordal_tables/{algorithm}_vs_dsatur_msc_avg_colors_comparison.png")

# Function to plot comparison for average colors used
def plot_comparison_with_dsatur_msc(file_paths):
    dsatur_msc_data = read_algorithm_data(file_paths["dsatur_msc"])
    dsatur_msc_avg_colors_used = [item[0] for item in dsatur_msc_data]

    for algorithm, file_path in file_paths.items():
        if algorithm == "dsatur_msc":
            continue

        algorithm_data = read_algorithm_data(file_path)
        algorithm_avg_colors_used = [item[0] for item in algorithm_data]

        fig, ax = plt.subplots(figsize=(8, 6))
        bar_width = 0.35
        index = np.arange(len(dsatur_msc_avg_colors_used))

        ax.bar(index, dsatur_msc_avg_colors_used, bar_width, label="DSATUR MSC", color='blue')
        ax.bar(index + bar_width, algorithm_avg_colors_used, bar_width, label=algorithm, color='green')
        
        ax.set_title(f"Comparison: Average Colors Used ({algorithm} vs DSATUR MSC)")
        ax.set_xlabel("Graph Number")
        ax.set_ylabel("Average Colors Used")
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(range(1, len(dsatur_msc_avg_colors_used) + 1))
        ax.legend()

        save_plot_with_check(algorithm, fig)

# Function to read execution time data
def read_algorithm_execution_time(file_path):
    execution_times = []
    with open(file_path, 'r') as f:
        for line in f:
            _, execution_time = line.strip().split(',')
            execution_times.append(float(execution_time))
    return execution_times

# Function to aggregate execution times by node count
def aggregate_execution_times(node_counts, execution_times):
    aggregated = defaultdict(list)
    for node, time in zip(node_counts, execution_times):
        aggregated[node].append(time)
    return {node: np.mean(times) for node, times in aggregated.items()}

# Function to plot execution time comparison
def plot_execution_time_comparison(file_paths, node_counts):
    fig, ax = plt.subplots(figsize=(10, 6))

    for algorithm, file_path in file_paths.items():
        execution_times = read_algorithm_execution_time(file_path)
        aggregated_times = aggregate_execution_times(node_counts, execution_times)
        
        sorted_node_counts = sorted(aggregated_times.keys())
        sorted_execution_times = [aggregated_times[node] for node in sorted_node_counts]
        
        ax.plot(sorted_node_counts, sorted_execution_times, marker='o', label=algorithm)

    ax.set_title('Execution Time Comparison Across Algorithms')
    ax.set_xlabel('Node Count')
    ax.set_ylabel('Average Execution Time (seconds)')
    ax.legend()
    ax.grid(True)

    save_plot_with_check("execution_time_comparison", fig)

# Example usage: Update the file paths to replace brute_force_coloring with dsatur_msc
file_paths = {
    "dsatur_msc": "statistics/dsatur_with_mcs_avg_colors_and_time.csv",
    "greedy_with_degree": "statistics/greedy_with_degree_avg_colors_and_time.csv",
    "greedy_basic": "statistics/greedy_basic_avg_colors_and_time.csv",
    "dsatur": "statistics/dsatur_avg_colors_and_time.csv"
}

# Node counts for each test
nodes = [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]
plot_comparison_with_dsatur_msc(file_paths)
plot_execution_time_comparison(file_paths,nodes)