# Maximum Independent Set (MIS) with QDeep Hybrid Solver

This project implements a Maximum Independent Set solver using the QDeep Hybrid Solver on popular graph datasets.

## Project Structure

```
├── MIS-QDeep/                    # Main solver code
│   ├── main.py                   # Simple example usage
│   ├── dataset_runner.py         # Dataset runner for standardized datasets
│   ├── generate_results_md.py    # Generate detailed results.md report with graphs
│   ├── utils.py                  # QUBO matrix generation utilities
│   ├── requirements.txt          # Python dependencies
│   ├── datasets_standardized/    # Standardized datasets (1-indexed)
│   │   ├── Zachary_Karate_Club.txt
│   │   ├── Dolphin_Social_Network.txt
│   │   ├── College_Football.txt
│   │   ├── Les_Miserables.txt
│   │   ├── Davis_Southern_Women.txt
│   │   ├── Myciel3_Graph.txt
│   │   ├── Myciel4_Graph.txt
│   │   ├── Myciel5_Graph.txt
│   │   └── Queen5_5_Graph.txt
│   └── Original datasets/        # Original datasets in various formats
│       ├── soc-karate/
│       ├── soc-dolphins/
│       ├── lesmis/
│       ├── misc-football/
│       └── download.tsv.*/
```

## Dataset Format

All datasets in `datasets_standardized/` use the consistent format:
```
nodes nodes edges
u1 v1
u2 v2
...
```

Where:
- First line: `nodes nodes edges` (node count, node count, edge count)
- Subsequent lines: Edge pairs (1-indexed node IDs)
- All nodes are 1-indexed (1, 2, 3, ...) to match the solver's expectations

## Running the Solver

### Quick Start
```bash
cd MIS-QDeep
python main.py
```

### Run on All Standardized Datasets
```bash
cd MIS-QDeep
python dataset_runner.py
```

This will:
- Process all datasets in `datasets_standardized/`
- Solve MIS for each graph
- Generate visualizations in `results/`
- Create summary reports (JSON and CSV)

### Generate Detailed Results Report
```bash
cd MIS-QDeep
python generate_results_md.py
```

This will:
- Process all datasets
- Generate QUBO matrices for each graph
- Create graph visualizations with MIS highlighted
- Create a comprehensive `results.md` file with:
  - Graph edge information
  - Complete QUBO matrix representation
  - MIS solution details
  - Energy values and validation
  - Graph visualizations embedded in the report

### Individual Dataset
```python
from dataset_runner import StandardizedMISRunner

runner = StandardizedMISRunner()
graph = runner.load_standardized_dataset("datasets_standardized/Zachary_Karate_Club.txt")
result = runner.solve_mis(graph, "Zachary_Karate_Club")
```

## Datasets Included

### Social Networks
- **Zachary Karate Club**: 34 nodes, 78 edges
- **Dolphin Social Network**: 62 nodes, 159 edges  
- **College Football**: 115 nodes, 613 edges
- **Les Miserables**: 77 nodes, 254 edges
- **Davis Southern Women**: 32 nodes, 89 edges

### DIMACS Challenge Graphs
- **Myciel3**: 11 nodes, 20 edges
- **Myciel4**: 23 nodes, 71 edges
- **Myciel5**: 47 nodes, 236 edges
- **Queen5_5**: 25 nodes, 320 edges

## Requirements

Install dependencies:
```bash
pip install -r MIS-QDeep/requirements.txt
```

## Results

The solver generates:
- **Graph visualizations**: PNG files with MIS nodes highlighted in red
- **JSON results**: Detailed results for each dataset
- **CSV summary**: Tabular results for analysis
- **Console output**: Real-time progress and statistics
- **results.md**: Comprehensive report with QUBO matrices and detailed analysis

## Notes

- Results include MIS size, solve time, and validity verification
- The `results.md` file provides complete QUBO matrix analysis for each dataset
