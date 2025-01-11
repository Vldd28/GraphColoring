import networkx as nx
import matplotlib.pyplot as plt

def visualize_colored_graph(graph, coloring):
    """
    Visualizes a graph with vertex coloring.
    
    Parameters:
        graph (dict): Adjacency list representation of the graph.
        coloring (dict): A dictionary mapping each vertex to its assigned color.
    """
    # Create a NetworkX graph
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Assign colors to nodes
    node_colors = [coloring[node] for node in G.nodes()]

    # Generate a colormap
    unique_colors = list(set(node_colors))
    cmap = plt.get_cmap("tab20")  # Tab20 has distinct colors
    color_map = {color: cmap(i / len(unique_colors)) for i, color in enumerate(unique_colors)}

    # Map node colors to actual colors
    mapped_colors = [color_map[color] for color in node_colors]

    # Draw the graph
    pos = nx.spring_layout(G, seed=42)  # Layout for graph positioning
    nx.draw(
        G, pos, with_labels=True, node_color=mapped_colors,
        edge_color="gray", node_size=800, font_size=10, font_color="black"
    )
    
    # Create a legend for colors
    legend_elements = [
        plt.Line2D([0], [0], marker="o", color="w", label=f"Color {color}", 
                   markerfacecolor=color_map[color], markersize=10)
        for color in unique_colors
    ]
    plt.legend(handles=legend_elements, loc="best")
    
    # Show the graph
    plt.title("Graph Coloring Visualization")
    plt.show()

# Example graph and coloring
