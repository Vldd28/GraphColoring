from visualize_graph import visualize_colored_graph

def welsh_powell_coloring(graph):
    """
    Welsh-Powell algorithm for graph coloring.
    
    Parameters:
        graph (dict): Adjacency list representation of the graph.
    
    Returns:
        dict: A dictionary mapping each vertex to its assigned color.
    """
    # Order vertices by decreasing degree
    vertices = sorted(graph.keys(), key=lambda v: len(graph[v]), reverse=True)
    colors = {v: -1 for v in graph}  # -1 means uncolored
    current_color = 0

    for vertex in vertices:
        if colors[vertex] == -1:  # Uncolored vertex
            # Assign current color to all uncolored vertices not adjacent to any already colored
            for v in vertices:
                if colors[v] == -1 and all(colors[neighbor] != current_color for neighbor in graph[v]):
                    colors[v] = current_color
            current_color += 1

    return colors
