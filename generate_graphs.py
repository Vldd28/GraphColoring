import csv
import random
import networkx as nx
import os

def generate_bipartite_graph_csv(dir_name, file_name, n, m):
    if m > n * (n - 1):
        raise ValueError("The number of edges exceeds the maximum possible for the given nodes.")
    set1 = set(range(n // 2))
    set2 = set(range(n // 2, n))
    possible_edges = [(x, y) for x in set1 for y in set2]
    edges = random.sample(possible_edges, m)
    os.makedirs(dir_name, exist_ok=True)  # Ensure the directory exists
    with open(os.path.join(dir_name, file_name), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([n, m])
        for edge in edges:
            writer.writerow(edge)

def generate_regular_graph_csv(dir_name, file_name, n, k):
    if k >= n or (n * k) % 2 != 0:
        raise ValueError("A k-regular graph is not possible with the given n and k.")
    adjacency_list = {i: set() for i in range(n)}
    nodes = list(range(n))
    for node in nodes:
        while len(adjacency_list[node]) < k:
            neighbor = random.choice(nodes)
            if neighbor != node and len(adjacency_list[neighbor]) < k and neighbor not in adjacency_list[node]:
                adjacency_list[node].add(neighbor)
                adjacency_list[neighbor].add(node)
    edges = set()
    for node, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            if (neighbor, node) not in edges:
                edges.add((node, neighbor))
    os.makedirs(dir_name, exist_ok=True)  # Ensure the directory exists
    with open(os.path.join(dir_name, file_name), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([n, len(edges)])
        for edge in edges:
            writer.writerow(edge)

def generate_planar_graph_csv(dir_name, file_name, n, m):
    max_edges = 3 * n - 6 if n > 2 else n * (n - 1) // 2
    if m > max_edges:
        raise ValueError("The number of edges exceeds the maximum possible for a planar graph.")
    possible_edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    edges = random.sample(possible_edges, m)
    os.makedirs(dir_name, exist_ok=True)  # Ensure the directory exists
    with open(os.path.join(dir_name, file_name), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([n, m])
        for edge in edges:
            writer.writerow(edge)

def generate_complete_graph_csv(dir_name, file_name, n):
    m = n * (n - 1) // 2
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    os.makedirs(dir_name, exist_ok=True)  # Ensure the directory exists
    with open(os.path.join(dir_name, file_name), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([n, m])
        for edge in edges:
            writer.writerow(edge)

import csv
import random
import os

def generate_chordal_graph_csv(dir_name, file_name, n, m):
    """
    Generează un graf cordal și îl salvează într-un fișier CSV.

    Parametri:
        dir_name (str): Numele directorului în care se va salva fișierul.
        file_name (str): Numele fișierului CSV de ieșire.
        n (int): Numărul de noduri.
        m (int): Numărul de muchii.

    Notă:
        Graful va fi cordal, dar este necesar să avem m >= n - 1
        pentru a forma cel puțin un arbore.
    """
    if m < n - 1:
        raise ValueError("Un graf cordal trebuie să aibă cel puțin n-1 muchii (arbore spanning).")

    # Pasul 1: Crearea unui arbore spanning (folosind DFS)
    edges = []
    for i in range(1, n):
        parent = random.randint(0, i - 1)
        edges.append((parent, i))
    
    # Pasul 2: Adăugarea muchiilor suplimentare pentru a atinge m
    added_edges = set(edges)
    while len(edges) < m:
        # Selectăm două noduri aleatorii
        u, v = random.sample(range(n), 2)
        if u > v:
            u, v = v, u
        # Adăugăm muchia doar dacă nu există deja și dacă păstrează proprietatea cordală
        if (u, v) not in added_edges:
            edges.append((u, v))
            added_edges.add((u, v))
    
    # Pasul 3: Crearea directorului dacă nu există
    os.makedirs(dir_name, exist_ok=True)
    
    # Pasul 4: Scrierea grafului în CSV
    with open(os.path.join(dir_name, file_name), mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Scriem numărul de noduri și muchii pe prima linie
        writer.writerow([n, len(edges)])
        
        # Scriem muchiile
        for edge in edges:
            writer.writerow(edge)

def generate_laman_graph_csv(dir_name, file_name, n):
    if n < 3:
        raise ValueError("A Laman graph requires at least 3 vertices.")
    m = 2 * n - 3
    adjacency_list = {i: set() for i in range(n)}
    edges = set()
    for i in range(1, n):
        edges.add((i - 1, i))
        adjacency_list[i - 1].add(i)
        adjacency_list[i].add(i - 1)
    while len(edges) < m:
        u, v = random.sample(range(n), 2)
        if v not in adjacency_list[u]:
            edges.add((u, v))
            adjacency_list[u].add(v)
            adjacency_list[v].add(u)
    os.makedirs(dir_name, exist_ok=True)  # Ensure the directory exists
    with open(os.path.join(dir_name, file_name), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([n, m])
        for edge in edges:
            writer.writerow(edge)

def generate_my_cielski_graph_csv(dir_name, file_name, n):
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if (i + j) % 2 == 1:
                G.add_edge(i, j)
    edges = list(G.edges())
    os.makedirs(dir_name, exist_ok=True)  # Ensure the directory exists
    with open(os.path.join(dir_name, file_name), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([n, len(edges)])
        for edge in edges:
            writer.writerow(edge)

def generate_prism_graph_csv(dir_name, file_name, n):
    G = nx.Graph()
    cycle1 = range(n)
    cycle2 = range(n, 2 * n)
    for i in range(n):
        G.add_edge(i, (i + 1) % n)
        G.add_edge(i + n, (i + 1) % n + n)
        G.add_edge(i, i + n)
    edges = list(G.edges())
    os.makedirs(dir_name, exist_ok=True)  # Ensure the directory exists
    with open(os.path.join(dir_name, file_name), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([n, len(edges)])
        for edge in edges:
            writer.writerow(edge)

def generate_dense_graph_csv(dir_name, file_name, n, m):
    G = nx.Graph()
    G.add_nodes_from(range(n))
    edges_added = 0
    while edges_added < m:
        u, v = random.sample(range(n), 2)
        if not G.has_edge(u, v):
            G.add_edge(u, v)
            edges_added += 1
    edges = list(G.edges())
    os.makedirs(dir_name, exist_ok=True)  # Ensure the directory exists
    with open(os.path.join(dir_name, file_name), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([n, len(edges)])
        for edge in edges:
            writer.writerow(edge)

import random

# Directory name for hard-to-compute graphs
# dir_name_hard = 'hard_to_compute'

# # Generate 50 random graphs for "hard-to-compute"
# n = 10
# for i in range(4):
#     n += 1
#     m = random.randint(n * (n - 1) // 4, n * (n - 1) // 2)  # Random number of edges, ensuring it's a dense graph
#     # Generate different types of graphs for hard-to-compute
#     generate_my_cielski_graph_csv(dir_name_hard, f"mycielski_graph_{i+1}.csv", n)
#     generate_prism_graph_csv(dir_name_hard, f"prism_graph_{i+1}.csv", n)
#     # generate_dense_graph_csv(dir_name_hard, f"dense_graph_{i+1}.csv", n, m)
#     n_low = n
#     m_low = random.randint(1, 3 * n_low - 6) if n_low > 2 else random.randint(1, n_low * (n_low - 1) // 2)
#     generate_planar_graph_csv(dir_name_hard, f"planar_graph_{i+1}.csv", n_low, m_low)

#     m_low = random.randint(1, 3 * n_low - 6) if n_low > 2 else random.randint(1, n_low * (n_low - 1) // 2)
#     generate_planar_graph_csv(dir_name_hard, f"planar_graph_{i+1}.csv", n_low, m_low)

#     m_low = random.randint(1, (n_low // 2) * (n_low // 2))
#     generate_bipartite_graph_csv(dir_name_hard, f"bipartite_graph_{i+1}.csv", n_low, m_low)

#     # generate_complete_graph_csv(dir_name_hard, f"complete_graph_{i+1}.csv", n_low)

#     generate_laman_graph_csv(dir_name_hard, f"laman_graph_{i+1}.csv", n_low)
dir_name_chordal = 'chordal_tests'
n = 50
for i in range(20):
    generate_chordal_graph_csv(dir_name_chordal,f"chordal_graph_{i+1}.csv",n,n+20)
    n=n+1
