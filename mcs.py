def mcs(graph):
    """
    Implementarea algoritmului MCS (Maximum Cardinality Search) pentru a obține
    un perfect elimination order (PEO) pentru un graf cordal.

    Parametri:
        graph (dict): Un graf reprezentat ca o listă de adiacență.
                      Cheile sunt nodurile, iar valorile sunt listele de vecini.

    Returnează:
        list: O listă care conține ordinea perfectă de eliminare (PEO).
    """
    # Inițializăm gradele de cardinalitate
    cardinality = {node: 0 for node in graph}
    visited = set()
    order = []

    while len(visited) < len(graph):
        # Alegem nodul cu cea mai mare cardinalitate care nu a fost vizitat
        max_node = max((node for node in graph if node not in visited), 
                       key=lambda x: cardinality[x])
        order.append(max_node)
        visited.add(max_node)

        # Actualizăm gradele de cardinalitate pentru vecinii neexplorați
        for neighbor in graph[max_node]:
            if neighbor not in visited:
                cardinality[neighbor] += 1

    return order
