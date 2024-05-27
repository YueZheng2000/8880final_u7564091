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

# Calculate the number of criminals per crime and plot
criminal_counts = [len(criminals) for criminals in case_to_criminals.values()]
average_criminals_per_crime = sum(criminal_counts) / len(criminal_counts)

# Distribution of criminals per crime
criminal_count_distribution = Counter(criminal_counts)
counts, frequencies = zip(*criminal_count_distribution.items())

# Plotting the histogram
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(counts, frequencies, color='g')
ax.set_title("Distribution of Number of Criminals in Each Crime")
ax.set_xlabel("Number of Criminals")
ax.set_ylabel("Frequency")
ax.set_xticks(counts)
ax.set_xticklabels([str(count) for count in counts])

plt.tight_layout()
plt.show()

# Print the average number of criminals per crime
print("Average Number of Criminals per Crime:", average_criminals_per_crime)
