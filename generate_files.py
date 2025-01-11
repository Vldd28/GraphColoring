import random
import csv

def generate_large_graph(num_vertices, num_edges, output_file):
    """
    Generates a random graph with a specified number of vertices and edges, 
    and saves it to a CSV file in adjacency list format.
    
    Parameters:
        num_vertices (int): The number of vertices in the graph.
        num_edges (int): The number of edges in the graph.
        output_file (str): The name of the CSV file to save the graph.
    """
    # Initialize the adjacency list as an empty dictionary
    graph = {i: [] for i in range(num_vertices)}

    # Randomly add edges
    while num_edges > 0:
        # Randomly choose two different vertices to connect
        v1 = random.randint(0, num_vertices - 1)
        v2 = random.randint(0, num_vertices - 1)

        # Ensure that the vertices are not the same and the edge doesn't already exist
        if v1 != v2 and v2 not in graph[v1]:
            graph[v1].append(v2)
            graph[v2].append(v1)  # Since it's an undirected graph
            num_edges -= 1

    # Save the graph to a CSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        for vertex, neighbors in graph.items():
            writer.writerow([vertex] + neighbors)

    print(f"Graph with {num_vertices} vertices and {num_edges} edges saved to {output_file}")

def load_graph_from_csv(input_file):
    """
    Loads a graph from a CSV file into an adjacency list format.
    
    Parameters:
        input_file (str): The name of the CSV file containing the graph.
    
    Returns:
        dict: A dictionary where each key is a vertex, and the value is a list of adjacent vertices.
    """
    graph = {}
    
    with open(input_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            vertex = int(row[0])  # The first element is the vertex
            neighbors = list(map(int, row[1:]))  # The rest are neighbors
            
            # Add the vertex and its neighbors to the graph
            graph[vertex] = neighbors
    
    print(f"Graph loaded from {input_file} with {len(graph)} vertices.")
    return graph

for i in range(10):
    generate_large_graph(1000,1000,"large_graph"+str(i)+".csv")

# # Example: Load the graph from the CSV file
# graph = load_graph_from_csv("large_graph.csv")

# # Print the graph structure (only showing a few entries for large graphs)
# for vertex, neighbors in list(graph.items())[:5]:  # Print the first 5 vertices
#     print(f"Vertex {vertex}: {neighbors}")
