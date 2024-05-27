import networkx as nx
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt


def random_walk_with_restart(G, start_node, restart_prob=0.15, tolerance=1e-6):
    if start_node not in G:
        print(f"Node {start_node} does not exist in the graph.")
        return {}

    nodes = list(G.nodes())
    node_index = nodes.index(start_node)

    # Initialize probability vector
    p = np.zeros(len(nodes))
    p[node_index] = 1

    # Transition matrix construction
    A = nx.to_numpy_array(G, nodelist=nodes, weight='weight', nonedge=0)
    row_sums = A.sum(axis=1, where=(A > 0))  # Avoid division by zero
    A = np.divide(A, row_sums[:, np.newaxis], where=(row_sums[:, np.newaxis] > 0))

    # Iteration with RWR
    while True:
        new_p = restart_prob * np.eye(len(nodes))[node_index] + (1 - restart_prob) * A.dot(p)
        if np.linalg.norm(new_p - p, 1) < tolerance:
            break
        p = new_p

    return dict(zip(nodes, p))


file_path = 'out.moreno_crime_crime'
G = nx.Graph()
criminal_to_cases = defaultdict(set)
case_to_criminals = defaultdict(set)

with open(file_path, 'r') as file:
    for line in file:
        if line.strip() and not line.startswith('%'):
            parts = line.split()
            criminal_id, case_id = int(parts[0]), int(parts[1])
            criminal_to_cases[criminal_id].add(case_id)
            case_to_criminals[case_id].add(criminal_id)

for criminal, cases in criminal_to_cases.items():
    G.add_node(criminal, size=len(cases))

for criminals in case_to_criminals.values():
    for criminal1 in criminals:
        for criminal2 in criminals:
            if criminal1 != criminal2:
                if G.has_edge(criminal1, criminal2):
                    G[criminal1][criminal2]['weight'] += 1
                else:
                    G.add_edge(criminal1, criminal2, weight=1)

print("Data Loaded. Number of Nodes in G:", G.number_of_nodes())  # Debugging print


# Function to calculate average RWR distances for a specific case
def average_rwr_distances_for_case(case_id):
    if case_id not in case_to_criminals:
        print(f"Case {case_id} does not exist.")
        return

    criminals_in_case = list(case_to_criminals[case_id])
    avg_distances = {}

    for criminal in criminals_in_case:
        rwr_result = random_walk_with_restart(G, criminal)
        if rwr_result:
            total_distance = 0
            for other_criminal in criminals_in_case:
                if other_criminal != criminal:
                    total_distance += rwr_result.get(other_criminal, 0)
            avg_distance = total_distance / (len(criminals_in_case) - 1)
            avg_distances[criminal] = avg_distance
        else:
            print(f"RWR computation failed for criminal {criminal}.")

    return avg_distances


# Example: Compute average RWR distances for a specific case
example_case_id = 42
avg_distances = average_rwr_distances_for_case(example_case_id)

print(f"Average RWR distances for case {example_case_id}:")
for criminal, avg_distance in avg_distances.items():
    print(f"Criminal {criminal}: {avg_distance:.4f}")

