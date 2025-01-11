from visualize_graph import visualize_colored_graph

def backtracking_coloring(graph):
    """
    Backtracking algorithm to solve the graph coloring problem.
    
    Parameters:
        graph (dict): Adjacency list representation of the graph.
    
    Returns:
        dict: A dictionary mapping each vertex to its assigned color.
              Returns None if no valid coloring exists.
    """
    # Initialize colors for each vertex (-1 means uncolored)
    colors = {v: -1 for v in graph}

    def is_valid(vertex, color):
        """Check if assigning 'color' to 'vertex' is valid."""
        for neighbor in graph[vertex]:
            if colors[neighbor] == color:  # Neighbor already has the same color
                return False
        return True

    def solve(vertex_index):
        """Recursive backtracking function."""
        # Base case: all vertices are colored
        if vertex_index == len(graph):
            return True
        
        # Get the vertex to color
        vertex = list(graph.keys())[vertex_index]

        # Try all colors
        for color in range(len(graph)):
            if is_valid(vertex, color):
                # Assign color and recurse
                colors[vertex] = color
                if solve(vertex_index + 1):
                    return True
                # Backtrack
                colors[vertex] = -1

        return False

    # Start backtracking from the first vertex
    if solve(0):
        return colors
    else:
        return None
