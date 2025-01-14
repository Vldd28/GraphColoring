from mcs import mcs

def dsatur_with_mcs(graph):
    """
    DSATUR algorithm applied in the order given by MCS.

    Parameters:
        graph (dict): The adjacency list of the graph.

    Returns:
        dict: A dictionary mapping vertices to their assigned color.
    """
    # Step 1: Get the MCS order
    peo = mcs(graph)  # Utilizează funcția MCS definită mai sus
    
    # Step 2: Initialize data structures for DSatur
    colors = {v: -1 for v in graph}  # -1 means uncolored
    
    # Step 3: Process nodes in MCS order
    for vertex in peo:
        # Find colors used by neighbors
        neighbor_colors = {colors[neighbor] for neighbor in graph[vertex] if colors[neighbor] != -1}
        # Assign the smallest available color
        color = 0
        while color in neighbor_colors:
            color += 1
        colors[vertex] = color
    return colors