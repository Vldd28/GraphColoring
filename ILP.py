from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value

from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value

def ilp_coloring(graph):
    """
    Integer Linear Programming for graph coloring.
    
    Parameters:
        graph (dict): Adjacency list representation of the graph.
    
    Returns:
        dict: A dictionary mapping each vertex to its assigned color.
    """
    # Problem definition
    num_vertices = len(graph)
    problem = LpProblem("Graph_Coloring", LpMinimize)

    # Variables: x[i][c] = 1 if vertex i is assigned color c
    x = {v: {c: LpVariable(f"x_{v}_{c}", 0, 1, cat="Binary") for c in range(num_vertices)} for v in graph}

    # Objective: minimize the maximum color used
    y = LpVariable("y", 0, num_vertices - 1, cat="Integer")  # Maximum color index
    problem += y

    # Constraints: every vertex must have one color
    for v in graph:
        problem += lpSum(x[v][c] for c in range(num_vertices)) == 1

    # Constraints: adjacent vertices must have different colors
    for v, neighbors in graph.items():
        for neighbor in neighbors:
            for c in range(num_vertices):
                problem += x[v][c] + x[neighbor][c] <= 1

    # Constraints: y is the maximum color used
    for v in graph:
        for c in range(num_vertices):
            problem += c * x[v][c] <= y

    # Solve the ILP
    problem.solve()

    # Extract solution
    colors = {v: next(c for c in range(num_vertices) if value(x[v][c]) == 1) for v in graph}
    return colors
