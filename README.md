# DAA Mini Project: Travelling Salesperson Problem (TSP)
## Comparative Performance and Optimality Analysis: Exact vs. Approximation Algorithms

**Subject:** Design and Analysis of Algorithms (DAA)  
**Academic Level:** 4th Year Computer Engineering  

---

## 📌 Project Overview
The Travelling Salesperson Problem (TSP) is an NP-hard problem in combinatorial optimization. This project provides a comparative performance benchmark and interactive visualization platform evaluating exact algorithms against polynomial-time approximation and heuristic algorithms.

### 🔬 Implemented Algorithms
1. **Held-Karp (Dynamic Programming with Bitmasking):**
   * Time Complexity: $O(n^2 \cdot 2^n)$
   * Space Complexity: $O(n \cdot 2^n)$
   * Guaranteed true mathematical optimal baseline.
2. **Branch and Bound (Reduced Cost Matrix):**
   * Time Complexity: Worst-case $O(n!)$, pruned average case
   * Space Complexity: $O(n^2 \cdot \text{depth})$
   * Explores state-space tree while pruning suboptimal branches via lower bound reductions.
3. **MST 2-Approximation (Christofides Preorder):**
   * Time Complexity: $O(n^2)$
   * Space Complexity: $O(n)$
   * Minimum Spanning Tree traversal with shortcut paths; theoretical upper bound $\le 2 \times \text{Optimal}$.
4. **Nearest Neighbour + 2-Opt Local Search:**
   * Time Complexity: $O(n^2)$
   * Space Complexity: $O(n)$
   * Greedy path construction followed by iterative 2-edge exchange local optimization to untangle intersecting paths.

---

## 📁 Repository Structure
```
├── data/
│   └── sample_tsplib/
│       └── eil51.tsp                # Standard TSPLIB 51-city benchmark instance
├── src/
│   ├── algorithms/
│   │   ├── base.py                  # Abstract base TSPSolver class
│   │   ├── exact_held_karp.py       # Held-Karp DP solver
│   │   ├── exact_branch_bound.py    # Branch & Bound solver with RCM
│   │   ├── approx_mst_2approx.py    # MST 2-Approximation solver
│   │   └── heuristic_2opt.py        # Nearest Neighbour + 2-Opt solver
│   ├── core/
│   │   ├── graph.py                 # 2D Euclidean graph & TSPLIB parser
│   │   └── benchmark.py             # Profiling engine (perf_counter, tracemalloc)
│   ├── visualizer/
│   │   ├── plot_tours.py            # 2D tour cycle plotter
│   │   └── plot_metrics.py          # Complexity scaling curves
│   └── app.py                       # Interactive Streamlit dashboard
├── tests/
│   └── test_solvers.py              # Pytest verification suite
├── results/
│   ├── benchmark_results.csv        # Benchmarking data
│   ├── benchmark_summary.json       # JSON export
│   ├── scaling_runtime.png          # Execution time scaling plot
│   └── scaling_cost.png             # Solution quality comparison plot
├── requirements.txt                 # Dependencies
├── main.py                          # CLI runner for batch benchmarks
└── README.md
```

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Test Suite
```bash
python -m pytest tests/ -v
```

### 3. Run Batch Benchmarking (CLI)
```bash
python main.py --sizes 5 8 10 12 --exact-limit 10
```

### 4. Launch Interactive Streamlit Dashboard (Viva Demo)
```bash
streamlit run src/app.py
```

---

## 📊 Sample Empirical Results

| Instance | $N$ | Algorithm | Tour Cost | Time (s) | Peak RAM (KB) | Approx Ratio |
|---|---|---|---|---|---|---|
| Random-8 | 8 | Held-Karp (Exact DP) | 2453.96 | 0.0145 s | 80.59 KB | 1.000 |
| Random-8 | 8 | Branch & Bound (RCM) | 2453.96 | 0.0286 s | 36.06 KB | 1.000 |
| Random-8 | 8 | MST 2-Approximation | 2958.05 | 0.0001 s | 1.86 KB | 1.205 |
| Random-8 | 8 | Nearest Neighbour + 2-Opt | 2453.96 | 0.0003 s | 0.31 KB | 1.000 |
| eil51 | 51 | MST 2-Approximation | 615.35 | 0.0018 s | 9.48 KB | 1.391 |
| eil51 | 51 | Nearest Neighbour + 2-Opt | 442.30 | 0.1441 s | 1.29 KB | 1.000 |

---

## 🎓 Viva Key Takeaways
1. **Exponential Wall:** For $N \ge 15$, exact algorithms hit computational thresholds where execution time and memory increase exponentially ($O(2^n)$ and $O(n!)$).
2. **Approximation Guarantees:** MST 2-Approximation runs in milliseconds ($O(n^2)$) and strictly guarantees solution cost $\le 2 \times \text{Optimal}$ under triangle inequality.
3. **2-Opt Performance:** Nearest Neighbour followed by 2-Opt local search untangles edge intersections and produces near-optimal solutions with minimal computational overhead.
