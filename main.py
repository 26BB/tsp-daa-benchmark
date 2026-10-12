import os
import argparse
import pandas as pd
from typing import List

from src.core.graph import TSPGraph
from src.core.benchmark import TSPBenchmark
from src.algorithms.exact_held_karp import HeldKarpSolver
from src.algorithms.exact_branch_bound import BranchAndBoundSolver
from src.algorithms.approx_mst_2approx import MST2ApproxSolver
from src.algorithms.heuristic_2opt import NearestNeighbour2OptSolver
from src.visualizer.plot_metrics import plot_runtime_scaling, plot_cost_comparison

def main():
    parser = argparse.ArgumentParser(description="DAA Mini Project: TSP Exact vs. Approximation Benchmarker")
    parser.add_argument("--sizes", nargs="+", type=int, default=[5, 8, 10, 12, 14, 16],
                        help="List of problem sizes N for synthetic testing")
    parser.add_argument("--tsplib", type=str, default="data/sample_tsplib/eil51.tsp",
                        help="Path to TSPLIB benchmark instance")
    parser.add_argument("--exact-limit", type=int, default=14,
                        help="Maximum N for exact algorithms to prevent exponential timeouts")
    args = parser.parse_args()

    print("======================================================================")
    print(" DAA Mini Project: Travelling Salesperson Problem (Exact vs Approx)")
    print("======================================================================")

    # 1. Initialize Solvers
    solvers = [
        HeldKarpSolver(),
        BranchAndBoundSolver(),
        MST2ApproxSolver(),
        NearestNeighbour2OptSolver()
    ]
    benchmark = TSPBenchmark(solvers)

    # 2. Build Dataset Suite
    graphs: List[TSPGraph] = []
    print(f"\n[+] Generating synthetic random Euclidean graphs for N = {args.sizes}...")
    for n in args.sizes:
        graphs.append(TSPGraph.generate_random(n, seed=42 + n))

    # Add TSPLIB if present
    if os.path.exists(args.tsplib):
        print(f"[+] Loading TSPLIB benchmark: {args.tsplib}")
        graphs.append(TSPGraph.from_tsplib(args.tsplib))

    # 3. Run Benchmark Suite
    print(f"\n[+] Running benchmark experiments (Exact limit N <= {args.exact_limit})...")
    df = benchmark.run_suite(graphs, exact_threshold=args.exact_limit)

    # 4. Display Results
    os.makedirs("results", exist_ok=True)
    summary_cols = ["instance", "n_cities", "algorithm", "cost", "time_sec", "peak_memory_kb", "approx_ratio", "is_valid"]
    print("\n[+] Benchmark Results Table:")
    print(df[summary_cols].to_string(index=False))

    # Save to CSV and JSON
    csv_path = "results/benchmark_results.csv"
    json_path = "results/benchmark_summary.json"
    df[summary_cols].to_csv(csv_path, index=False)
    df[summary_cols].to_json(json_path, orient="records", indent=2)
    print(f"\n[+] Results saved to:\n    - {csv_path}\n    - {json_path}")

    # 5. Generate and Save Comparative Plots
    print("\n[+] Generating complexity scaling curves...")
    plot_runtime_scaling(df, save_path="results/scaling_runtime.png")
    plot_cost_comparison(df, save_path="results/scaling_cost.png")
    print("    - results/scaling_runtime.png")
    print("    - results/scaling_cost.png")
    print("\n[OK] Benchmarking completed successfully!")

if __name__ == "__main__":
    main()
