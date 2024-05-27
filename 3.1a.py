import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import collections  # Import the collections module for Counter

file_path = 'out.moreno_crime_crime'

# Create a new graph where nodes represent criminals
G = nx.Graph()

# Read data and build mappings from criminals to cases and vice versa
criminal_to_cases = defaultdict(set)
case_to_criminals = defaultdict(set)

with open(file_path, 'r') as file:
    for line in file:
        if line.strip() and not line.startswith('%'):
            parts = line.split()
            criminal_id = int(parts[0])
            case_id = int(parts[1])
            criminal_to_cases[criminal_id].add(case_id)
            case_to_criminals[case_id].add(criminal_id)

# Add nodes and edges, recording the number of cases each criminal is involved in as a node attribute
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

# Basic Network Properties
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
average_degree = sum(dict(G.degree()).values()) / float(num_nodes)
density = nx.density(G)
clustering_coefficient = nx.average_clustering(G)

# Print network properties
print("Number of Nodes:", num_nodes)
print("Number of Edges:", num_edges)
print("Average Degree:", average_degree)
print("Density:", density)
print("Average Clustering Coefficient:", clustering_coefficient)

# Visualization setup
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, scale=2, seed=42)
weights = [G[u][v]['weight']*0.5 for u, v in G.edges()]
node_sizes = [G.nodes[node]['size']*1 for node in G.nodes()]
nx.draw_networkx(G, pos, node_size=node_sizes, node_color='blue', with_labels=False, width=weights, edge_color='gray')
plt.title('Network of Criminals with Shared Cases')
plt.show()
