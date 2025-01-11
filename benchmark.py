import time
import random
from visualize_graph import visualize_colored_graph
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value
import math
import networkx as nx
from bkt_coloring import backtracking_coloring
from genetic_algorithm_coloring import genetic_algorithm_coloring
from ILP import ilp_coloring
from simulated_annealing_coloring import simulated_annealing_coloring
from welsh_powell_coloring import welsh_powell_coloring
from Dsatur import dsatur
# Validation function to check if the coloring is valid
def validate_coloring(graph, coloring):
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            if coloring[vertex] == coloring[neighbor]:
                return False
    return True

# Benchmarking function with argument flexibility
def benchmark_algorithms(algorithms, graphs, num_colors=3, repetitions=5):
    results = {}

    for algorithm in algorithms:
        results[algorithm.__name__] = []

        for graph in graphs:
            # Run each algorithm multiple times
            times = []
            for _ in range(repetitions):
                # Determine the number of arguments the algorithm expects
                num_args = algorithm.__code__.co_argcount

                # Start the timer
                start_time = time.time()

                # Run the algorithm based on the number of arguments it takes
                if num_args == 1:  # Algorithm takes only 'graph'
                    colors = algorithm(graph)
                elif num_args == 2:  # Algorithm takes 'graph' and 'num_colors'
                    colors = algorithm(graph, num_colors)

                end_time = time.time()
                times.append(end_time - start_time)

                # Validate the coloring
                is_valid = validate_coloring(graph, colors)

                # Visualize the result
                if is_valid:
                    visualize_colored_graph(graph, colors)

            # Average time for current algorithm
            avg_time = sum(times) / repetitions
            results[algorithm.__name__].append({
                "avg_time": avg_time,
                "valid": is_valid,
                "num_colors": len(set(colors.values()))
            })

    return results

# Example list of graphs (you can add more graphs or load from a file)
graphs = [
    {0: [1, 2], 1: [0, 2, 3], 2: [0, 1, 3], 3: [1, 2]},  # Graph 1
    # Add other graphs here
]

# List of algorithms to benchmark
algorithms = [
    backtracking_coloring,
    # genetic_algorithm_coloring,
    # ilp_coloring,
    # simulated_annealing_coloring,
    # welsh_powell_coloring,
    dsatur
]

# Run the benchmark
results = benchmark_algorithms(algorithms, graphs, num_colors=3)

# Print results
for algo_name, res in results.items():
    print(f"Results for {algo_name}:")
    for i, result in enumerate(res):
        print(f"  Graph {i + 1}: Avg Time = {result['avg_time']} seconds, Valid = {result['valid']}, Colors = {result['num_colors']}")
