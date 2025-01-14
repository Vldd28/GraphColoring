def dsatur(graph):
    """
    DSATUR algorithm for graph coloring.
    
    Parameters:
        graph (dict): The adjacency list of the graph.
    
    Returns:
        dict: A dictionary mapping vertices to their assigned color.
    """
    colors = {v: -1 for v in graph}  # -1 means uncolored
    saturation_degree = {v: 0 for v in graph}  # Tracks saturation degree
    degrees = {v: len(neighbors) for v, neighbors in graph.items()}  # Vertex degrees
    
    def update_saturation(vertex):
        adjacent_colors = {colors[neighbor] for neighbor in graph[vertex] if colors[neighbor] != -1}
        saturation_degree[vertex] = len(adjacent_colors)
    
    uncolored_vertices = set(graph.keys())
    
    while uncolored_vertices:
        # Select the vertex with the highest saturation degree, breaking ties with degree
        vertex = max(uncolored_vertices, key=lambda v: (saturation_degree[v], degrees[v]))
        uncolored_vertices.remove(vertex)
        
        # Update saturation degree of its neighbors
        for neighbor in graph[vertex]:
            if neighbor in uncolored_vertices:
                update_saturation(neighbor)
        
        # Assign the smallest available color
        neighbor_colors = {colors[neighbor] for neighbor in graph[vertex] if colors[neighbor] != -1}
        color = 0
        while color in neighbor_colors:
            color += 1
        colors[vertex] = color
    
    return colors
