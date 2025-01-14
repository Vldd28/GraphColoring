import random
import csv

def load_graph_from_csv(input_file):
    """
    Loads a graph from a CSV file into an adjacency list format.
    The file format expects the first line to contain the number of vertices and edges,
    and subsequent lines to define the edges in the format (u, v).
    
    Parameters:
        input_file (str): The name of the CSV file containing the graph.
    
    Returns:
        dict: A dictionary where each key is a vertex, and the value is a list of adjacent vertices.
    """
    graph = {}

    with open(input_file, mode='r') as file:
        reader = csv.reader(file)
        
        # Read the first line (number of vertices and edges)
        n, m = map(int, next(reader))
        print(f"Graph has {n} vertices and {m} edges.")
        
        # Initialize the graph with empty adjacency lists for all vertices
        for i in range(n):
            graph[i] = []

        # Read the edges and populate the adjacency list
        for row in reader:
            u, v = map(int, row)
            
            # Ensure that both vertices exist in the graph
            if u >= n or v >= n:
                print(f"Warning: Edge ({u}, {v}) references invalid vertex, skipping.")
                continue
            
            # Add the edge to the adjacency list (undirected graph)
            graph[u].append(v)
            graph[v].append(u)

    return graph

def main():
    pass
if __name__ == "__main__":
    main()
