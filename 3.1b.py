import networkx as nx
from collections import defaultdict, Counter
import matplotlib.pyplot as plt

file_path = 'out.moreno_crime_crime'

# Initialize graph and data structures
G = nx.Graph()
criminal_to_cases = defaultdict(set)
case_to_criminals = defaultdict(set)

# Data loading
with open(file_path, 'r') as file:
    for line in file:
        if line.strip() and not line.startswith('%'):
            parts = line.split()
            criminal_id, case_id = int(parts[0]), int(parts[1])
            criminal_to_cases[criminal_id].add(case_id)
            case_to_criminals[case_id].add(criminal_id)

# Node and edge setup
for criminal, cases in criminal_to_cases.items():
    G.add_node(criminal, size=len(cases))
for case, criminals in case_to_criminals.items():
    criminals = list(criminals)
    for i in range(len(criminals)):
        for j in range(i + 1, len(criminals)):
            if G.has_edge(criminals[i], criminals[j]):
                G[criminals[i]][criminals[j]]['weight'] += 1
            else:
                G.add_edge(criminals[i], criminals[j], weight=1)

# Setup for plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
degreeCount = Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())

# Degree plot
ax1.bar(deg, cnt, width=0.80, color='b')
ax1.set_title("Degree Histogram")
ax1.set_ylabel("Count")
ax1.set_xlabel("Degree")
ax1.set_xticks(deg[::5])
ax1.set_xticklabels([str(d) for d in deg[::5]])  # Labels not rotated

# Weight plot
edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
weight_counts = Counter(edge_weights)
weights, counts = zip(*weight_counts.items())
ax2.bar(weights, counts, width=0.80, color='r')
ax2.set_title("Edge Weight Distribution")
ax2.set_ylabel("Count")
ax2.set_xlabel("Weight of Edges")
ax2.set_xticks(weights)
ax2.set_xticklabels(weights)  # Labels not rotated

plt.tight_layout()
plt.show()
