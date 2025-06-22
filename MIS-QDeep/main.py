import os 
import networkx as nx
from dotenv import load_dotenv
from qdeepsdk import QDeepHybridSolver
from utils import mis_qubo_matrix, is_independent_set
import matplotlib.pyplot as plt

# Load environment variables from .env file
load_dotenv()

solver = QDeepHybridSolver()
solver.token = os.getenv("TOKEN")

# Default values for the solver
solver.m_budget = 50000
solver.num_reads = 10000

# Example graph (can be replaced with any graph)
graph = nx.Graph()
graph.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (1, 5)])


Q, nodes = mis_qubo_matrix(graph, penalty=2)
response = solver.solve(Q)

result = response["QdeepHybridSolver"]
config = result["configuration"]
energy = result["energy"]
mis_nodes = [nodes[i] for i, val in enumerate(config) if round(val) == 1]

print(Q)
print("Configuration:", config)
print("Energy:", energy)
print("Maximum Independent Set Nodes:", mis_nodes)
print(is_independent_set(graph, mis_nodes))

# Visualize the graph in an image with the maximum independent set highlighted
plt.figure(figsize=(8, 6))
colors = ['red' if node in mis_nodes else 'lightgray' for node in graph.nodes()]
nx.draw(graph, with_labels=True, node_color=colors, node_size=1000, font_size=16, font_weight='bold')
plt.title("Input Graph")
plt.savefig(f"graph.png")
plt.close()
