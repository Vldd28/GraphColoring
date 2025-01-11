from visualize_graph import visualize_colored_graph


def dsatur(graph):
    """
    DSatur algorithm for graph coloring.
    
    Parameters:
        graph (dict): Adjacency list representation of the graph.
                      Keys are vertices, and values are lists of adjacent vertices.
    
    Returns:
        colors (dict): A dictionary mapping each vertex to its assigned color.
    """
    # Initialize variables
    num_vertices = len(graph)
    colors = {v: -1 for v in graph}  # -1 means uncolored
    saturation = {v: 0 for v in graph}  # Saturation degree for each vertex
    degrees = {v: len(graph[v]) for v in graph}  # Degree of each vertex

    # Select the first vertex to color (highest degree)
    current_vertex = max(graph, key=lambda v: degrees[v])

    colors[current_vertex] = 0  # Assign the first color
    available_colors = {v: set(range(num_vertices)) for v in graph}  # All possible colors
    available_colors[current_vertex].remove(0)

    # Update saturation for neighbors
    for neighbor in graph[current_vertex]:
        saturation[neighbor] += 1
        if 0 in available_colors[neighbor]:
            available_colors[neighbor].remove(0)

    # Color remaining vertices
    for _ in range(num_vertices - 1):
        # Select the next vertex based on saturation (tie-breaking by degree)
        current_vertex = max(
            graph,
            key=lambda v: (saturation[v], degrees[v]) if colors[v] == -1 else (-1, -1)
        )

        # Assign the smallest available color
        chosen_color = min(available_colors[current_vertex])
        colors[current_vertex] = chosen_color

        # Update available colors for neighbors and saturation
        for neighbor in graph[current_vertex]:
            if colors[neighbor] == -1 and chosen_color in available_colors[neighbor]:
                available_colors[neighbor].remove(chosen_color)
                saturation[neighbor] = len(set(colors[n] for n in graph[neighbor] if colors[n] != -1))

    return colors
