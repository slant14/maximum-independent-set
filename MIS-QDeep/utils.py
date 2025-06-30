import numpy as np

def mis_qubo_matrix(graph, penalty=2):
    """Generate the QUBO matrix for the MIS of a given graph."""
    nodes = sorted(graph.nodes())  # Get consistent node ordering
    n = len(nodes)
    node_to_index = {node: i for i, node in enumerate(nodes)}
    
    # Initialize QUBO matrix
    Q = np.zeros((n, n))
    
    # Add linear terms (diagonal): -1 to maximize each vertex
    for i in range(n):
        Q[i, i] = -1.0
    
    # Add quadratic terms (off-diagonal): penalty for connected vertices
    for u, v in graph.edges():
        i, j = node_to_index[u], node_to_index[v]
        min_idx, max_idx = min(i, j), max(i, j)
        Q[min_idx, max_idx] = penalty
    
    return Q, nodes


def is_independent_set(graph, node_list):
    node_set = set(node_list)
    for node in node_list:
        for neighbor in graph.neighbors(node):
            if neighbor in node_set:
                return False
    return True