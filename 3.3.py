import networkx as nx
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

def random_walk_with_restart(G, start_node, restart_prob=0.15, tolerance=1e-6):
    if start_node not in G:
        print(f"Node {start_node} does not exist in the graph.")
        return {}

    nodes = list(G.nodes())
    if start_node in nodes:
        node_index = nodes.index(start_node)
    else:
        print(f"Node index for {start_node} not found.")
        return {}

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
            criminal_id, case_id = int(parts[0]), int(parts[1])  # Ensure IDs are treated as integers
            criminal_to_cases[criminal_id].add(case_id)
            case_to_criminals[case_id].add(criminal_id)

for criminal, cases in criminal_to_cases.items():
    G.add_node(criminal, size=len(cases))  # Nodes added as integers

for criminals in case_to_criminals.values():
    for criminal1 in criminals:
        for criminal2 in criminals:
            if criminal1 != criminal2:
                if G.has_edge(criminal1, criminal2):
                    G[criminal1][criminal2]['weight'] += 1
                else:
                    G.add_edge(criminal1, criminal2, weight=1)

# Check for node '100'
if 100 in G:
    rwr_result = random_walk_with_restart(G, 100)  # Use 100 as an integer
    if rwr_result:
        sorted_rwr = sorted(rwr_result.items(), key=lambda x: x[1], reverse=True)
        top_5_related_nodes = sorted_rwr[1:6]  # Exclude the first one because it's the node itself
        print("Top 5 nodes closely associated with node 100 based on RWR:")
        for node, prob in top_5_related_nodes:
            print(f"Node {node} with RWR probability {prob:.4f}")
    else:
        print("RWR computation failed or returned an empty result.")
else:
    print("Node 100 is not in the network.")

