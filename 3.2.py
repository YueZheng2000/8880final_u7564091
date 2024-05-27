import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

file_path = 'out.moreno_crime_crime'

# Create a new graph where nodes represent cases
G = nx.Graph()

# Read the data and establish a mapping from cases to criminals
case_to_criminals = defaultdict(set)
criminal_to_cases = defaultdict(set)
with open(file_path, 'r') as file:
    for line in file:
        if line.strip() and not line.startswith('%'):
            parts = line.split()
            criminal_id = int(parts[0])
            case_id = int(parts[1])
            case_to_criminals[case_id].add(criminal_id)
            criminal_to_cases[criminal_id].add(case_id)

# Function to calculate the minimum number of criminals covering 80% of the cases
def find_minimal_criminals_covering_80_percent(case_to_criminals):
    total_cases = len(case_to_criminals)  # Total number of cases
    needed_coverage = total_cases * 0.8  # Minimum number of cases to cover

    # Calculate the number of cases each criminal is involved in
    criminal_to_cases = defaultdict(set)
    for case, criminals in case_to_criminals.items():
        for criminal in criminals:
            criminal_to_cases[criminal].add(case)

    # Sort criminals by the number of cases they are involved in
    sorted_criminals = sorted(criminal_to_cases.items(), key=lambda x: len(x[1]), reverse=True)

    # Select criminals until the covered cases reach 80%
    selected_criminals = []
    covered_cases = set()
    for criminal, cases in sorted_criminals:
        if len(covered_cases) >= needed_coverage:
            break
        if not covered_cases.issuperset(cases):  # Only select the criminal if new cases are added
            covered_cases.update(cases)
            selected_criminals.append(criminal)

    return selected_criminals, len(covered_cases) / total_cases

# Call the function to compute
selected_criminals, coverage = find_minimal_criminals_covering_80_percent(case_to_criminals)
print(len(selected_criminals))
print(f"Selected criminals: {selected_criminals}")
print(f"Coverage: {coverage*100:.2f}%")

# Create the graph
G = nx.Graph()

# Add nodes and edges, recording the number of cases each criminal is involved in as a node attribute
for criminal, cases in criminal_to_cases.items():
    G.add_node(criminal, size=len(cases))  # The 'size' attribute stores the number of cases

# Add edges based on the number of shared cases
for criminals in case_to_criminals.values():
    for criminal1 in criminals:
        for criminal2 in criminals:
            if criminal1 != criminal2:
                if G.has_edge(criminal1, criminal2):
                    G[criminal1][criminal2]['weight'] += 1
                else:
                    G.add_edge(criminal1, criminal2, weight=1)

# Set the criminals to be highlighted in red
highlight_criminals = set(selected_criminals)

# Set a fixed random seed
np.random.seed(42)

# Visualize the network
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, scale=2, seed=42)  # Set a fixed random seed
weights = [G[u][v]['weight']*0.5 for u, v in G.edges()]  # Adjust edge width using weights

# Retrieve all nodes and set colors
node_colors = ['red' if node in highlight_criminals else 'blue' for node in G.nodes()]
node_sizes = [5 if node in highlight_criminals else 1 for node in G.nodes()]

nx.draw_networkx(G, pos, node_size=node_sizes, node_color=node_colors, with_labels=False, width=weights, edge_color='gray')
plt.title('Network of Criminals with Shared Cases')
plt.show()
