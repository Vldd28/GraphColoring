import math
import random
from visualize_graph import visualize_colored_graph
import math
import random

def simulated_annealing_coloring(graph, initial_temp=1000, cooling_rate=0.99, max_iter=1000):
    """
    Simulated Annealing for Graph Coloring.
    
    Parameters:
        graph (dict): Adjacency list representation of the graph.
        initial_temp (float): Starting temperature.
        cooling_rate (float): Rate of temperature decrease.
        max_iter (int): Maximum number of iterations.
    
    Returns:
        dict: A dictionary mapping each vertex to its assigned color.
    """
    def calculate_cost(coloring):
        """Calculate the number of conflicting edges."""
        conflicts = 0
        for vertex, neighbors in graph.items():
            for neighbor in neighbors:
                if coloring[vertex] == coloring[neighbor]:
                    conflicts += 1
        return conflicts

    def get_neighbor(coloring):
        """Generate a neighboring solution by modifying one vertex's color."""
        neighbor = coloring.copy()
        vertex = random.choice(list(graph.keys()))
        neighbor[vertex] = random.randint(0, len(graph) - 1)
        return neighbor

    # Initialize with a random solution
    current_solution = {v: random.randint(0, len(graph) - 1) for v in graph}
    current_cost = calculate_cost(current_solution)
    temperature = initial_temp

    for _ in range(max_iter):
        if temperature <= 0 or current_cost == 0:
            break

        # Generate a new neighbor solution
        neighbor = get_neighbor(current_solution)
        neighbor_cost = calculate_cost(neighbor)

        # Accept the neighbor based on probability
        if neighbor_cost < current_cost or random.random() < math.exp((current_cost - neighbor_cost) / temperature):
            current_solution, current_cost = neighbor, neighbor_cost

        # Decrease the temperature
        temperature *= cooling_rate

    return current_solution
