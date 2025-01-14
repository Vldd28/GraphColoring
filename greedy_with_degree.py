def greedy_with_degree(graph):
    """
    Greedy algorithm for graph coloring using the degree heuristic.
    
    Parameters:
        graph (dict): The adjacency list of the graph.
    
    Returns:
        dict: A dictionary mapping vertices to their assigned color.
    """
    colors = {v: -1 for v in graph}  # -1 means uncolored
    
    # Sort vertices by degree in descending order
    sorted_vertices = sorted(graph, key=lambda v: len(graph[v]), reverse=True)
    
    for vertex in sorted_vertices:
        # Get the set of colors of neighboring vertices
        neighbor_colors = {colors[neighbor] for neighbor in graph[vertex] if colors[neighbor] != -1}
        
        # Assign the smallest available color
        color = 0
        while color in neighbor_colors:
            color += 1
        colors[vertex] = color
    
    return colors
