import itertools

def brute_force_coloring(graph):
    """
    Completely brute-force algorithm for graph coloring.
    Tries all possible colorings of the graph, checking each one for validity.
    """
    nodes = list(graph.keys())  # Get the list of nodes from the graph
    num_nodes = len(nodes)
    
    # Try all possible colorings by considering every combination of color assignments
    for num_colors in range(1, num_nodes + 1):
        # Generate all possible color assignments for the nodes (color combinations)
        color_combinations = itertools.product(range(num_colors), repeat=num_nodes)
        
        for coloring in color_combinations:
            coloring_dict = dict(zip(nodes, coloring))
            # Check if the coloring is valid
            if validate_coloring(graph, coloring_dict):
                return coloring_dict  # Return the first valid coloring found

    return None  # If no valid coloring is found

def validate_coloring(graph, coloring):
    """
    Validate a coloring solution.

    Parameters:
        graph (dict): Adjacency list of the graph.
        coloring (dict): Vertex-to-color mapping.

    Returns:
        bool: True if the coloring is valid, False otherwise.
    """
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            if coloring[vertex] == coloring[neighbor]:  # Two adjacent nodes have the same color
                return False

    return True
