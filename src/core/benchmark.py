import time
import tracemalloc
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd

from src.algorithms.base import TSPSolver
from src.core.graph import TSPGraph

class TSPBenchmark:
    """
    Benchmarking engine to profile execution time, peak memory usage,
    tour validity, and approximation ratios.
    """

    def __init__(self, solvers: List[TSPSolver]):
        self.solvers = solvers

    def benchmark_single(self, solver: TSPSolver, graph: TSPGraph, timeout_sec: float = 60.0) -> Dict[str, Any]:
        """
        Runs one solver on one graph and measures:
        - time (seconds) via time.perf_counter
        - peak memory (KB) via tracemalloc
        - tour validity
        - cost
        """
        tracemalloc.start()
        start_time = time.perf_counter()

        try:
            cost, tour, stats = solver.solve(graph.dist_matrix)
            elapsed_time = time.perf_counter() - start_time
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            is_valid = TSPSolver.is_valid_tour(tour, graph.n)

            return {
                "instance": graph.name,
                "n_cities": graph.n,
                "algorithm": solver.name,
                "cost": round(cost, 2),
                "time_sec": round(elapsed_time, 5),
                "peak_memory_kb": round(peak_mem / 1024.0, 2),
                "is_valid": is_valid,
                "tour": tour,
                "stats": stats,
                "error": None
            }

        except Exception as e:
            tracemalloc.stop()
            return {
                "instance": graph.name,
                "n_cities": graph.n,
                "algorithm": solver.name,
                "cost": None,
                "time_sec": None,
                "peak_memory_kb": None,
                "is_valid": False,
                "tour": [],
                "stats": {},
                "error": str(e)
            }

    def run_suite(self, graphs: List[TSPGraph], exact_threshold: int = 18) -> pd.DataFrame:
        """
        Runs all solvers across multiple graphs.
        Automatically skips exponential exact algorithms for graphs with n > exact_threshold.
        Computes approximation ratios relative to optimal or best heuristic.
        """
        records = []

        for graph in graphs:
            ground_truth_cost = None

            for solver in self.solvers:
                is_exact = "Exact" in solver.name or "Branch" in solver.name

                if is_exact and graph.n > exact_threshold:
                    continue  # Skip exponential solvers for large N

                result = self.benchmark_single(solver, graph)
                records.append(result)

                # Track exact baseline if available
                if solver.name == "Held-Karp (Exact DP)" and result["cost"] is not None:
                    ground_truth_cost = result["cost"]

        df = pd.DataFrame(records)

        # Calculate Approximation Ratios
        if not df.empty:
            approx_ratios = []
            for _, row in df.iterrows():
                inst = row["instance"]
                inst_rows = df[(df["instance"] == inst) & (df["cost"].notna())]
                
                # Check if exact DP cost exists for this instance
                exact_row = inst_rows[inst_rows["algorithm"] == "Held-Karp (Exact DP)"]
                if not exact_row.empty:
                    base_cost = exact_row.iloc[0]["cost"]
                else:
                    base_cost = inst_rows["cost"].min()

                if row["cost"] is not None and base_cost and base_cost > 0:
                    approx_ratios.append(round(row["cost"] / base_cost, 3))
                else:
                    approx_ratios.append(None)

            df["approx_ratio"] = approx_ratios

        return df
