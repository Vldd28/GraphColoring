import sentry_sdk
import time
from dsatur import dsatur
from greedy_basic import greedy_basic
from greedy_with_degree import greedy_with_degree
from generate_files import load_graph_from_csv
from brute_force import brute_force_coloring
from dsatur_mcs import dsatur_with_mcs
import sys
import os
sys.setrecursionlimit(3000)  # Adjust the value as needed

# Initialize Sentry with performance monitoring
sentry_sdk.init(
    dsn="https://7539de94667225b7e498b507329ac24d@o4508625078059008.ingest.de.sentry.io/4508627055280208",
    traces_sample_rate=1.0,  # Adjust the sampling rate for performance data
)

def validate_coloring(graph, coloring, max_colors=None):
    """
    Validate a coloring solution.

    Parameters:
        graph (dict): Adjacency list of the graph.
        coloring (dict): Vertex-to-color mapping.
        max_colors (int, optional): Maximum allowed number of colors.

    Returns:
        bool: True if the coloring is valid, False otherwise.
    """
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            if coloring[vertex] == coloring[neighbor]:
                return False

    # Validate the range of colors, if max_colors is provided
    if max_colors is not None:
        if any(color < 0 or color >= max_colors for color in coloring.values()):
            return False

    return True

def print_coloring_result_to_file(graph, coloring, file):
    """
    Print the coloring result in the specified format to a file.
    The first line is the minimum number of colors, the second line is the coloring of the nodes.
    
    Parameters:
        graph (dict): The graph represented as an adjacency list.
        coloring (dict): The coloring solution represented as a dictionary mapping nodes to colors.
        file (file object): The file object to write the result to.
    """
    # Calculate the minimum number of colors used
    unique_colors = set(coloring.values())  # Get unique colors used
    min_colors = len(unique_colors)  # The number of unique colors is the answer to the first line
    
    # Write the minimum number of colors
    file.write(f"{min_colors}\n")
    
    # Prepare the color assignments in the correct order (nodes should be printed in the order they appear in the graph)
    coloring_values = [coloring[node] for node in graph]
    
    # Write the color assignments of the nodes
    file.write(" ".join(map(str, coloring_values)) + "\n")

def benchmark_algorithms_with_sentry(algorithms, graphs, repetitions=1):
    results = {}
    statistics = {}  # To store statistics for each algorithm

    # Open the output file for writing the results
    with open('out.txt', 'w') as file:
        for algorithm in algorithms:
            results[algorithm.__name__] = []
            statistics[algorithm.__name__] = {
                "total_tests": 0,
                "successful_tests": 0,
                "avg_time": 0,
                "avg_colors_used": 0  # Ensure avg_colors_used is initialized
            }

            # Create a separate file for average colors used and execution time for each algorithm
            with open(f"statistics/{algorithm.__name__}_avg_colors_and_time.csv", 'w') as avg_colors_file:
                for graph_idx, graph in enumerate(graphs):
                    # Use a Sentry transaction for each graph-algorithm combination
                    with sentry_sdk.start_transaction(op="benchmark", name=f"{algorithm.__name__}_Graph{graph_idx+1}"):

                        times = []
                        successful_runs = 0
                        colors_used = []

                        for _ in range(repetitions):
                            # Start a span for individual runs
                            with sentry_sdk.start_span(op="run", description=f"Run {algorithm.__name__}"):

                                start_time = time.time()
                                colors = algorithm(graph)
                                end_time = time.time()

                                # Debugging print statements
                                print(f"{algorithm.__name__} Graph {graph_idx+1} result: {colors}")
                                
                                times.append(end_time - start_time)

                                # Validate the coloring
                                is_valid = validate_coloring(graph, colors)
                                print(f"Validation result for {algorithm.__name__}: {is_valid}")
                                
                                if is_valid:
                                    successful_runs += 1
                                    colors_used.append(len(set(colors.values())))

                                    # Write the result to the file when the coloring is valid
                                    print_coloring_result_to_file(graph, colors, file)

                        # Calculate average time, success rate, and average colors used
                        avg_time = sum(times) / repetitions
                        success_rate = (successful_runs / repetitions) * 100
                        avg_colors_used = sum(colors_used) / len(colors_used) if colors_used else 0

                        # Store results
                        results[algorithm.__name__].append({
                            "graph": graph_idx + 1,
                            "avg_time": avg_time,
                            "valid": bool(successful_runs),
                            "success_rate": success_rate,
                            "avg_colors_used": avg_colors_used
                        })

                        # Write the average colors used and execution time for this graph to the algorithm-specific file
                        avg_colors_file.write(f"{avg_colors_used},"
                                              f"{avg_time}\n")

                        # Update statistics
                        statistics[algorithm.__name__]["total_tests"] += repetitions
                        statistics[algorithm.__name__]["successful_tests"] += successful_runs
                        statistics[algorithm.__name__]["avg_time"] += avg_time
                        statistics[algorithm.__name__]["avg_colors_used"] += avg_colors_used

        # Calculate overall average time and colors used
        for algo in statistics:
            statistics[algo]["avg_time"] /= len(graphs)  # Average across graphs
            statistics[algo]["avg_colors_used"] /= len(graphs)  # Average across graphs

    return results, statistics

# List of algorithms to benchmark
import matplotlib.pyplot as plt

# Assuming `statistics` contains the average time and colors used for each algorithm
def plot_statistics(statistics):
    algorithms = list(statistics.keys())  # List of algorithm names
    avg_times = [statistics[algo]["avg_time"] for algo in algorithms]
    avg_colors = [statistics[algo]["avg_colors_used"] for algo in algorithms]

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Plot average time
    ax1.bar(algorithms, avg_times, color='skyblue')
    ax1.set_title("Average Time per Algorithm")
    ax1.set_xlabel("Algorithms")
    ax1.set_ylabel("Average Time (seconds)")
    ax1.set_xticklabels(algorithms, rotation=45)

    # Plot average colors used
    ax2.bar(algorithms, avg_colors, color='lightgreen')
    ax2.set_title("Average Colors Used per Algorithm")
    ax2.set_xlabel("Algorithms")
    ax2.set_ylabel("Average Colors Used")
    ax2.set_xticklabels(algorithms, rotation=45)

    plt.tight_layout()
    plt.savefig("fig.png")

def load_graphs_from_directory(directory):
    """
    Loads all graphs from CSV files in the specified directory.
    
    Parameters:
        directory (str): The path to the directory containing the graph files.
    
    Returns:
        list: A list of dictionaries, each representing a graph.
    """
    graphnames = os.listdir(directory)
    graphs = []

    # Iterate through each file in the directory
    for filename in graphnames:
        if filename.endswith('.csv'):  # Make sure to load only .csv files
            graph = load_graph_from_csv(os.path.join(directory, filename))  # Load the graph
            graphs.append(graph)  # Add the graph to the list
    
    return graphs

# Now, call this function after getting the benchmark results
algorithms = [
    dsatur_with_mcs,
    # brute_force_coloring,
    dsatur,
    greedy_with_degree,
    greedy_basic
]
graphs = load_graphs_from_directory("chordal_tests")
# Run benchmarks with Sentry monitoring
results, statistics = benchmark_algorithms_with_sentry(algorithms, graphs)

# Print results
for algo_name, res in results.items():
    print(f"Results for {algo_name}:")
    for result in res:
        print(f"  Graph {result['graph']}: Avg Time = {result['avg_time']}s, "
              f"Success Rate = {result['success_rate']}%, Valid = {result['valid']}, "
              f"Avg Colors Used = {result['avg_colors_used']}")
