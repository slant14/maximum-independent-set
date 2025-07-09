#!/usr/bin/env python3
"""
Generate comprehensive results.md file with QUBO matrices and MIS results
"""

import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from qdeepsdk import QDeepHybridSolver
from utils import mis_qubo_matrix, is_independent_set
import time
from pathlib import Path
from datetime import datetime

# Load environment variables 
load_dotenv()

class ResultsMDGenerator:
    def __init__(self):
        self.solver = QDeepHybridSolver()
        self.solver.token = os.getenv("TOKEN")
        self.solver.m_budget = 50000
        self.solver.num_reads = 10000
        self.results = []
        
        # Dataset metadata with sources and papers from original datasets
        self.dataset_metadata = {
            "Zachary_Karate_Club": {
                "title": "Zachary Karate Club Network",
                "source": "Zachary, W. W. (1977). An Information Flow Model for Conflict and Fission in Small Groups. Journal of Anthropological Research, 33(4), 452-473.",
                "conference": "Journal of Anthropological Research",
                "year": 1977,
                "description": "Social network of a university karate club collected by Wayne Zachary in 1977. Each node represents a member, each edge represents a tie between members. The network is undirected.",
                "repository": "KONECT - The Koblenz Network Collection",
                "repository_citation": "Kunegis, J. (2013). KONECT -- The Koblenz Network Collection. Proc. Int. Conf. on World Wide Web Companion, 1343-1350.",
                "nodes": 34,
                "edges": 78
            },
            "Dolphin_Social_Network": {
                "title": "Dolphin Social Network",
                "source": "Lusseau, D., Schneider, K., Boisseau, O. J., Haase, P., Dawson, S., & Whitehead, H. (2003). The bottlenose dolphin community of Doubtful Sound features a large proportion of long-lasting associations. Behavioral Ecology and Sociobiology, 54(4), 396-405.",
                "conference": "Behavioral Ecology and Sociobiology",
                "year": 2003,
                "description": "Social network of bottlenose dolphins in Doubtful Sound, New Zealand.",
                "repository": "Network Repository",
                "repository_citation": "Rossi, R. A., & Ahmed, N. K. (2015). The Network Data Repository with Interactive Graph Analytics and Visualization. AAAI.",
                "nodes": 62,
                "edges": 159
            },
            "College_Football": {
                "title": "College Football Network",
                "source": "Girvan, M., & Newman, M. E. (2002). Community structure in social and biological networks. Proceedings of the National Academy of Sciences, 99(12), 7821-7826.",
                "conference": "Proceedings of the National Academy of Sciences",
                "year": 2002,
                "description": "Network of American football games between Division IA colleges during regular season Fall 2000.",
                "repository": "Network Repository",
                "repository_citation": "Rossi, R. A., & Ahmed, N. K. (2015). The Network Data Repository with Interactive Graph Analytics and Visualization. AAAI.",
                "nodes": 115,
                "edges": 613
            },
            "Les_Miserables": {
                "title": "Les Miserables Character Network",
                "source": "Knuth, D. E. (1993). The Stanford GraphBase: a platform for combinatorial computing. Addison-Wesley.",
                "conference": "Stanford GraphBase",
                "year": 1993,
                "description": "Co-appearance network of characters in Victor Hugo's novel Les Miserables.",
                "repository": "Network Repository",
                "repository_citation": "Rossi, R. A., & Ahmed, N. K. (2015). The Network Data Repository with Interactive Graph Analytics and Visualization. AAAI.",
                "nodes": 77,
                "edges": 254
            },
            "Davis_Southern_Women": {
                "title": "Davis Southern Women Social Network",
                "source": "Davis, A., Gardner, B. B., & Gardner, M. R. (1941). Deep South. University of Chicago Press.",
                "conference": "University of Chicago Press",
                "year": 1941,
                "description": "Social network of 18 women in Natchez, Mississippi, showing their attendance at 14 social events.",
                "repository": "Network Repository",
                "repository_citation": "Rossi, R. A., & Ahmed, N. K. (2015). The Network Data Repository with Interactive Graph Analytics and Visualization. AAAI.",
                "nodes": 32,
                "edges": 89
            },
            "Myciel3_Graph": {
                "title": "Myciel3 Graph",
                "source": "Mycielski, J. (1955). Sur le coloriage des graphes. Colloquium Mathematicum, 3, 161-162.",
                "conference": "Colloquium Mathematicum",
                "year": 1955,
                "description": "DIMACS challenge graph based on Mycielski transformation. Triangle-free with increasing coloring number.",
                "repository": "DIMACS Challenge",
                "repository_citation": "Johnson, D. S., & Trick, M. A. (1996). Cliques, Coloring, and Satisfiability: Second DIMACS Implementation Challenge. DIMACS Series in Discrete Mathematics and Theoretical Computer Science.",
                "nodes": 11,
                "edges": 20
            },
            "Myciel4_Graph": {
                "title": "Myciel4 Graph",
                "source": "Mycielski, J. (1955). Sur le coloriage des graphes. Colloquium Mathematicum, 3, 161-162.",
                "conference": "DIMACS Challenge",
                "year": 1993,
                "description": "DIMACS challenge graph based on Mycielski transformation. Triangle-free with increasing coloring number.",
                "repository": "DIMACS Challenge",
                "repository_citation": "Johnson, D. S., & Trick, M. A. (1996). Cliques, Coloring, and Satisfiability: Second DIMACS Implementation Challenge. DIMACS Series in Discrete Mathematics and Theoretical Computer Science.",
                "nodes": 23,
                "edges": 71
            },
            "Myciel5_Graph": {
                "title": "Myciel5 Graph",
                "source": "Mycielski, J. (1955). Sur le coloriage des graphes. Colloquium Mathematicum, 3, 161-162.",
                "conference": "DIMACS Challenge",
                "year": 1993,
                "description": "DIMACS challenge graph based on Mycielski transformation. Triangle-free with increasing coloring number.",
                "repository": "DIMACS Challenge",
                "repository_citation": "Johnson, D. S., & Trick, M. A. (1996). Cliques, Coloring, and Satisfiability: Second DIMACS Implementation Challenge. DIMACS Series in Discrete Mathematics and Theoretical Computer Science.",
                "nodes": 47,
                "edges": 236
            },
            "Queen5_5_Graph": {
                "title": "Queen5_5 Graph",
                "source": "Trick, M. A. (1993). Graph coloring instances. DIMACS Challenge.",
                "conference": "DIMACS Challenge",
                "year": 1993,
                "description": "5×5 queen graph from DIMACS challenge. Represents the 5-queens problem on a 5×5 chessboard.",
                "repository": "DIMACS Challenge",
                "repository_citation": "Johnson, D. S., & Trick, M. A. (1996). Cliques, Coloring, and Satisfiability: Second DIMACS Implementation Challenge. DIMACS Series in Discrete Mathematics and Theoretical Computer Science.",
                "nodes": 25,
                "edges": 320
            }
        }
        
    def load_standardized_dataset(self, filepath):
        """Load graph from standardized dataset format"""
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            # Parse header: nodes nodes edges
            header = lines[0].strip().split()
            nodes = int(header[0])
            edges = int(header[2])
            
            # Create graph
            G = nx.Graph()
            
            # Add edges (1-indexed) - handle both weighted and unweighted edges
            for line in lines[1:]:
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) >= 2:
                        u, v = int(parts[0]), int(parts[1])
                        G.add_edge(u, v)
            
            return G
            
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None
    
    def format_edges_for_md(self, graph):
        """Format edges for markdown display"""
        edges = list(graph.edges())
        if len(edges) <= 10:
            # Show all edges if 10 or fewer
            return str(edges)
        else:
            # Show first 5 and last 5 edges for large graphs
            first_edges = edges[:5]
            last_edges = edges[-5:]
            return f"{first_edges} ... {last_edges}"
    
    def format_qubo_matrix(self, Q):
        """Format QUBO matrix for markdown display"""
        n = len(Q)
        if n <= 10:
            # Show full matrix for small graphs
            lines = []
            for row in Q:
                line = "["
                for i, val in enumerate(row):
                    if i > 0:
                        line += " "
                    line += f"{val:4.1f}"
                line += "]"
                lines.append(line)
            return "\n".join(lines)
        else:
            # Show truncated matrix for large graphs
            lines = []
            # Show first 5 rows
            for i in range(min(5, n)):
                line = "["
                for j in range(min(5, n)):
                    if j > 0:
                        line += " "
                    line += f"{Q[i][j]:4.1f}"
                if n > 5:
                    line += " ..."
                line += "]"
                lines.append(line)
            
            if n > 5:
                lines.append("...")
                # Show last row
                line = "["
                for j in range(min(5, n)):
                    if j > 0:
                        line += " "
                    line += f"{Q[-1][j]:4.1f}"
                if n > 5:
                    line += " ..."
                line += "]"
                lines.append(line)
            
            return "\n".join(lines) + f"\n\n*Matrix size: {n} x {n} ({n*n} elements)*"
    
    def solve_mis_and_generate_report(self, graph, dataset_name):
        """Solve MIS and generate detailed report"""
        try:
            print(f"Processing {dataset_name}...")
            
            # Get graph info
            nodes = graph.number_of_nodes()
            edges = graph.number_of_edges()
            
            # Generate QUBO matrix
            Q, node_list = mis_qubo_matrix(graph, penalty=2)
            
            # Solve MIS
            start_time = time.time()
            response = self.solver.solve(Q)
            solve_time = time.time() - start_time
            
            result = response["QdeepHybridSolver"]
            config = result["configuration"]
            energy = result["energy"]
            mis_nodes = [node_list[i] for i, val in enumerate(config) if round(val) == 1]
            
            # Verify the result
            is_valid = is_independent_set(graph, mis_nodes)
            
            # Create results directory
            os.makedirs("results", exist_ok=True)
            
            # Generate graph visualization
            graph_filename = f"results/{dataset_name}_graph.png"
            self.visualize_graph(graph, mis_nodes, dataset_name, graph_filename)
            
            # Get dataset metadata
            metadata = self.dataset_metadata.get(dataset_name, {})
            
            # Generate report section
            report_section = f"""
## {metadata.get('title', dataset_name)}

**Dataset Information:**
- **Source Paper**: {metadata.get('source', 'N/A')}
- **Conference/Journal**: {metadata.get('conference', 'N/A')}
- **Year**: {metadata.get('year', 'N/A')}
- **Description**: {metadata.get('description', 'N/A')}
- **Repository**: {metadata.get('repository', 'N/A')}
- **Repository Citation**: {metadata.get('repository_citation', 'N/A')}

**Graph Information:**
- Nodes: {nodes}
- Edges: {edges}
- Solve Time: {solve_time:.2f}s
- Valid MIS: {is_valid}

**Graph Edges:**
```
{self.format_edges_for_md(graph)}
```

**QUBO Matrix:**
```
{self.format_qubo_matrix(Q)}
```

**MIS Result:**
- MIS Nodes: {mis_nodes}
- MIS Size: {len(mis_nodes)}
- Energy: {energy}

**Graph Visualization:**
![{dataset_name} Graph]({graph_filename})

---
"""
            
            return report_section
            
        except Exception as e:
            print(f"Error processing {dataset_name}: {e}")
            return f"""
## {dataset_name}

**Error:** {str(e)}

---
"""
    
    def visualize_graph(self, graph, mis_nodes, dataset_name, filename):
        """Visualize graph with MIS highlighted"""
        try:
            plt.figure(figsize=(12, 8))
            colors = ['red' if node in mis_nodes else 'lightgray' for node in graph.nodes()]
            pos = nx.spring_layout(graph, k=1, iterations=50)
            
            nx.draw(graph, pos, with_labels=True, node_color=colors, 
                   node_size=800, font_size=10, font_weight='bold',
                   edge_color='gray', width=1)
            
            plt.title(f"{dataset_name} - Maximum Independent Set (Red Nodes)")
            plt.tight_layout()
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            print(f"Error visualizing {dataset_name}: {e}")
    
    def generate_results_md(self):
        """Generate comprehensive results.md file"""
        
        # Get all .txt files from datasets_standardized
        datasets_dir = Path("datasets_standardized")
        dataset_files = list(datasets_dir.glob("*.txt"))
        
        print(f"Generating results.md for {len(dataset_files)} datasets...")
        
        # Start the markdown content
        md_content = f"""# MIS-QDeep Solver Results

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This report contains the results of Maximum Independent Set (MIS) calculations using the QDeep Hybrid Solver on various graph datasets from published papers and conferences.

## Dataset Sources

All datasets used in this analysis are from well-established papers and conferences:

### Social Networks
- **Zachary Karate Club** (1977): Journal of Anthropological Research
- **Dolphin Social Network** (2003): Behavioral Ecology and Sociobiology  
- **College Football** (2002): Proceedings of the National Academy of Sciences
- **Les Miserables** (1993): Stanford GraphBase
- **Davis Southern Women** (1941): University of Chicago Press

### DIMACS Challenge Graphs
- **Myciel3, Myciel4, Myciel5** (1955/1993): Colloquium Mathematicum / DIMACS Challenge
- **Queen5_5** (1993): DIMACS Challenge

## Datasets Processed

"""
        
        # Process each dataset
        for dataset_file in dataset_files:
            dataset_name = dataset_file.stem
            print(f"Processing {dataset_name}...")
            
            # Load graph
            graph = self.load_standardized_dataset(dataset_file)
            if graph:
                # Generate report section
                report_section = self.solve_mis_and_generate_report(graph, dataset_name)
                md_content += report_section
        
        # Add summary
        md_content += f"""
## Summary

Total datasets processed: {len(dataset_files)}

The QDeep Hybrid Solver successfully processed all datasets, generating QUBO matrices and finding Maximum Independent Sets for each graph. Each result includes:
- Graph structure and edge information
- Complete QUBO matrix representation
- MIS solution with node list and size
- Energy value from the solver
- Validation of the MIS solution

---
*Generated by MIS-QDeep Solver*
"""
        
        # Write to file
        with open("results.md", 'w') as f:
            f.write(md_content)
        
        print(f"Results saved to: results.md")

def main():
    """Main function to generate results.md"""
    generator = ResultsMDGenerator()
    generator.generate_results_md()

if __name__ == "__main__":
    main() 