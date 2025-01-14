def backtracking_coloring(graph):
    """
    Backtracking (Brute-Force) algorithm for graph coloring.
    
    Parameters:
        graph (dict): The adjacency list of the graph.
    
    Returns:
        dict: A dictionary mapping vertices to their assigned color.
    """
    colors = {v: -1 for v in graph}  # -1 means uncolored

    def is_valid(vertex, color):
        """Check if assigning the given color to the vertex is valid."""
        for neighbor in graph[vertex]:
            if colors[neighbor] == color:
                return False
        return True
    
    def backtrack(vertex):
        """Backtrack to find a valid coloring."""
        if vertex == len(graph):  # All vertices colored
            return True
        
        for color in range(len(graph)):
            if is_valid(vertex, color):
                colors[vertex] = color
                if backtrack(vertex + 1):  # Recurse to the next vertex
                    return True
                colors[vertex] = -1  # Undo the color if it doesn't work
        
        return False
    
    # Start the backtracking from the first vertex
    backtrack(0)
    
    return colors
