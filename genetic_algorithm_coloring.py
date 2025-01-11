import random
from visualize_graph import visualize_colored_graph

def genetic_algorithm_coloring(graph, population_size=50, generations=100, mutation_rate=0.1):
    """
    Genetic Algorithm for Graph Coloring.
    
    Parameters:
        graph (dict): Adjacency list representation of the graph.
        population_size (int): Size of the population.
        generations (int): Number of generations.
        mutation_rate (float): Probability of mutation.
    
    Returns:
        dict: A dictionary mapping each vertex to its assigned color.
    """
    def fitness(chromosome):
        """Calculate fitness based on the number of valid edges."""
        conflicts = 0
        for vertex, neighbors in graph.items():
            for neighbor in neighbors:
                if chromosome[vertex] == chromosome[neighbor]:
                    conflicts += 1
        return -conflicts

    def mutate(chromosome):
        """Mutate a random vertex's color."""
        vertex = random.choice(list(graph.keys()))
        chromosome[vertex] = random.randint(0, len(graph) - 1)

    def crossover(parent1, parent2):
        """Create offspring by combining two parents."""
        point = random.randint(0, len(parent1) - 1)
        child = {k: (parent1[k] if i <= point else parent2[k]) for i, k in enumerate(graph)}
        return child

    # Initialize population with random colorings
    population = [
        {v: random.randint(0, len(graph) - 1) for v in graph} for _ in range(population_size)
    ]

    # Run evolution
    for _ in range(generations):
        # Calculate fitness for each chromosome
        population = sorted(population, key=fitness, reverse=True)
        next_gen = population[:population_size // 2]  # Elitism: retain the top 50%

        # Generate new population through crossover
        for _ in range(population_size - len(next_gen)):
            parent1, parent2 = random.sample(next_gen, 2)
            child = crossover(parent1, parent2)
            if random.random() < mutation_rate:
                mutate(child)
            next_gen.append(child)

        population = next_gen

    # Return the best solution
    return population[0]
