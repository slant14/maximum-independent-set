#!/usr/bin/env python3
"""
Standardized Dataset Runner for MIS-QDeep Solver
Works with datasets_standardized/ folder containing properly formatted datasets
"""

import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
from qdeepsdk import QDeepHybridSolver
from utils import mis_qubo_matrix, is_independent_set
import time
import json
from pathlib import Path
import pandas as pd

# Load environment variables
load_dotenv()

class StandardizedMISRunner:
    def __init__(self):
        self.solver = QDeepHybridSolver()
        self.solver.token = os.getenv("TOKEN")
        self.solver.m_budget = 50000
        self.solver.num_reads = 10000
        self.results = []
        
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
            
            print(f"Loaded: {nodes} nodes, {edges} edges, actual edges: {G.number_of_edges()}")
            return G
            
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None
    
    def solve_mis(self, graph, dataset_name):
        """Solve MIS for a given graph"""
        try:
            print(f"\nSolving MIS for {dataset_name}")
            print(f"Graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
            
            # No size limit - let the solver handle any graph size
            
            start_time = time.time()
            Q, nodes = mis_qubo_matrix(graph, penalty=2)
            response = self.solver.solve(Q)
            
            result = response["QdeepHybridSolver"]
            config = result["configuration"]
            energy = result["energy"]
            mis_nodes = [nodes[i] for i, val in enumerate(config) if round(val) == 1]
            
            solve_time = time.time() - start_time
            
            # Verify the result
            is_valid = is_independent_set(graph, mis_nodes)
            
            result_data = {
                "dataset": dataset_name,
                "nodes": graph.number_of_nodes(),
                "edges": graph.number_of_edges(),
                "mis_size": len(mis_nodes),
                "mis_nodes": mis_nodes,
                "energy": energy,
                "solve_time": solve_time,
                "is_valid": is_valid
            }
            
            print(f"MIS size: {len(mis_nodes)}")
            print(f"Solve time: {solve_time:.2f}s")
            print(f"Valid MIS: {is_valid}")
            
            return result_data
            
        except Exception as e:
            print(f"Error solving MIS for {dataset_name}: {e}")
            return None
    
    def visualize_graph(self, graph, mis_nodes, dataset_name):
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
            
            # Create results directory
            os.makedirs("results", exist_ok=True)
            plt.savefig(f"results/{dataset_name}_graph.png", dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            print(f"Error visualizing {dataset_name}: {e}")
    
    def run_all_datasets(self):
        """Run MIS on all standardized datasets"""
        
        # Create results directory
        os.makedirs("results", exist_ok=True)
        
        # Get all .txt files from datasets_standardized
        datasets_dir = Path("datasets_standardized")
        dataset_files = list(datasets_dir.glob("*.txt"))
        
        print("Starting MIS evaluation on standardized datasets...")
        print("=" * 60)
        print(f"Found {len(dataset_files)} datasets")
        
        for dataset_file in dataset_files:
            dataset_name = dataset_file.stem
            print(f"\n{'='*40}")
            print(f"Processing: {dataset_name}")
            print(f"File: {dataset_file}")
            
            # Load graph
            graph = self.load_standardized_dataset(dataset_file)
            if graph:
                # Solve MIS
                result = self.solve_mis(graph, dataset_name)
                if result:
                    self.results.append(result)
                    # Visualize
                    self.visualize_graph(graph, result['mis_nodes'], dataset_name)
        
        print(f"\n{'='*60}")
        print(f"Completed evaluation of {len(self.results)} datasets")
        
        # Generate summary report
        self.generate_summary_report()
    
    def generate_summary_report(self):
        """Generate a summary report of all results"""
        if not self.results:
            print("No results to report")
            return
        
        # Create DataFrame for easy analysis
        df = pd.DataFrame(self.results)
        
        print("\n" + "="*60)
        print("SUMMARY REPORT")
        print("="*60)
        
        # Basic statistics
        print(f"Total datasets processed: {len(self.results)}")
        print(f"Average MIS size: {df['mis_size'].mean():.2f}")
        print(f"Average solve time: {df['solve_time'].mean():.2f}s")
        print(f"Valid MIS solutions: {df['is_valid'].sum()}/{len(df)}")
        
        # Detailed results
        print("\nDetailed Results:")
        print("-" * 80)
        print(f"{'Dataset':<20} {'Nodes':<6} {'Edges':<6} {'MIS Size':<8} {'Time(s)':<8} {'Valid':<6}")
        print("-" * 80)
        
        for result in self.results:
            print(f"{result['dataset']:<20} {result['nodes']:<6} {result['edges']:<6} "
                  f"{result['mis_size']:<8} {result['solve_time']:<8.2f} {str(result['is_valid']):<6}")
        
        # Save results to JSON
        with open("results/mis_results.json", 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Save results to CSV
        df.to_csv("results/mis_results.csv", index=False)
        
        print(f"\nResults saved to:")
        print(f"  - results/mis_results.json")
        print(f"  - results/mis_results.csv")
        print(f"  - results/*_graph.png (visualizations)")

def main():
    """Main function to run the standardized dataset evaluation"""
    runner = StandardizedMISRunner()
    runner.run_all_datasets()

if __name__ == "__main__":
    main() 