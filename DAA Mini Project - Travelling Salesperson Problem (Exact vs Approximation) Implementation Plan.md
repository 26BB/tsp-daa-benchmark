# **DAA Mini Project: Travelling Salesperson Problem (Exact vs. Approximation Algorithms)**

# **Academic Context**

* **Subject:** Design and Analysis of Algorithms (DAA)  
* **Level:** 4th Year Computer Engineering  
* **Project Title:** Comparative Performance and Optimality Analysis of Exact and Approximation Algorithms for the Travelling Salesperson Problem (TSP)

# **1\. Project Justification & Academic Rationale**

Among standard mini-project options (such as multithreaded matrix multiplication, multithreaded merge sort, and string matching with Naive/Rabin-Karp), the Travelling Salesperson Problem (TSP) is the strongest choice for a final-year DAA curriculum:

* **Direct Syllabus Alignment:** Multithreaded sorting and matrix multiplication primarily benchmark OS/HPC thread overhead and parallel cache locality rather than algorithm design. String matching (Naive vs. Rabin-Karp) is an introductory 2nd/3rd year laboratory practical. TSP directly covers core DAA theoretical foundations: NP-Hardness, state space tree pruning, exponential exact algorithms, and polynomial-time approximation ratios.  
* **Comprehensive Comparative Scope:** Contrasts exact solutions (guaranteed optimal, exponential time) against approximation heuristics (polynomial time, bounded error). Allows profiling execution time, peak memory usage, and solution quality across varying input sizes.  
* **High Viva Evaluation Value:** External examiners focus on algorithmic trade-offs between computational complexity and solution optimality, which TSP showcases effectively.

# **2\. Algorithm Scope & Complexity Matrix**

| Category | Algorithm | Time Complexity | Space Complexity | Description & Role |
| :---- | :---- | :---- | :---- | :---- |
| **Exact** | Held-Karp (Dynamic Programming) | O(n² · 2ⁿ) | O(n · 2ⁿ) | Finds the true optimal tour cost using bitmask memoization. Serves as ground truth baseline for n ≤ 20\. |
| **Exact / Pruning** | Branch and Bound (Reduced Cost Matrix) | Worst-case O(n\!), pruned average | O(n² · state tree depth) | State-space tree exploration with lower-bound matrix reductions to demonstrate practical search space pruning. |
| **Approximation** | 2-Approximation via MST (Preorder Traversal) | O(n²) | O(n) | Construct minimum spanning tree, perform Eulerian/preorder traversal with triangle inequality shortcuts. Guarantees tour cost ≤ 2 · Optimal. |
| **Heuristic** | Nearest Neighbour \+ 2-Opt Local Search | O(n²) | O(n) | Greedy construction followed by iterative 2-edge exchange local optimization to eliminate path crossovers. |

# **3\. Project Architecture & Directory Layout**

tsp-daa-project/

├── data/

│   ├── sample\_tsplib/

│   │   └── eil51.tsp

│   └── synthetic/

├── src/

│   ├── \_\_init\_\_.py

│   ├── algorithms/

│   │   ├── \_\_init\_\_.py

│   │   ├── base.py                 \# Abstract base class TSPSolver

│   │   ├── exact\_held\_karp.py      \# DP with bitmasking: O(n^2 \* 2^n)

│   │   ├── exact\_branch\_bound.py   \# State space tree with Reduced Cost Matrix

│   │   ├── approx\_mst\_2approx.py   \# Metric 2-Approximation via MST preorder

│   │   └── heuristic\_2opt.py       \# Nearest Neighbour \+ 2-Opt Local Search

│   ├── core/

│   │   ├── \_\_init\_\_.py

│   │   ├── graph.py                \# Graph model, Euclidean matrix, TSPLIB parser

│   │   └── benchmark.py            \# Profiler (perf\_counter, tracemalloc, ratio)

│   ├── visualizer/

│   │   ├── \_\_init\_\_.py

│   │   ├── plot\_tours.py           \# 2D node & tour cycle renderer

│   │   └── plot\_metrics.py         \# Scaling plots: Time vs N, Cost vs N

│   └── app.py                      \# Interactive Streamlit dashboard

├── tests/

│   ├── test\_solvers.py             \# Unit tests for cycle validity & triangle inequality

│   └── test\_benchmark.py

├── results/

│   ├── benchmark\_results.csv

│   └── benchmark\_summary.json

├── requirements.txt

├── README.md

└── main.py                         \# CLI entry point for batch benchmarking

# **4\. Benchmark & Evaluation Methodology**

## **Datasets**

* **Synthetic 2D Euclidean Graphs:** Uniformly distributed random points with sizes N in \[5, 8, 10, 12, 15, 18, 20, 30, 50\].  
* **Standard Benchmark Datasets:** TSPLIB instances (e.g., eil51, kroA100) using EUC\_2D format.

## **Performance Metrics**

1. **Execution Time (seconds/milliseconds):** High-precision wall-clock time via `time.perf_counter()`.  
2. **Peak Memory Consumption (KB/MB):** Tracked using Python `tracemalloc` module.  
3. **Approximation Ratio:**  
   * Approximation Ratio \= Cost\_approx / Cost\_optimal (for n ≤ 20).  
   * Relative Ratio \= Cost\_approx / Cost\_best\_heuristic (for n \> 20).  
4. **Tour Validity:** Automated verification that each vertex is visited exactly once and the cycle returns to the start vertex.

# **5\. Visual Demonstrations & Deliverables**

1. **Interactive Dashboard (Streamlit):** Node generator allowing live adjustment of graph size N, algorithm selector for real-time comparison, and side-by-side visualization of generated tour paths.  
2. **Visual Path Comparison:** 2D plots highlighting crossovers in naive/MST tours vs. uncrossed paths in optimal/2-Opt tours.  
3. **Complexity Scaling Curves:** Log-scale plot of Execution Time vs. Number of Nodes (N) to illustrate the exponential barrier of exact methods compared to polynomial heuristics.  
4. **Documentation & Report:** Algorithm formulations, pseudo-code, mathematical proof of the 2-approximation factor under triangle inequality, and empirical benchmarking tables.

# **6\. Implementation Prompt for Autonomous Agent**

## **TASK: Build a Complete TSP Exact vs. Approximation Benchmarking Suite**

**Objective**  
Build a modular, production-grade Python CLI and interactive benchmarking suite for the Travelling Salesperson Problem (TSP) for an undergraduate Design and Analysis of Algorithms (DAA) mini-project.

**Requirements**

1. Implement 2 exact algorithms (Held-Karp Dynamic Programming, Branch & Bound with Reduced Cost Matrix) and 2 approximation/heuristic algorithms (MST 2-Approximation, Nearest Neighbour \+ 2-Opt).  
2. Implement `TSPSolver` abstract base class returning `(best_cost, tour, stats)`.  
3. Build benchmark engine recording execution time, peak memory, tour validity, and approximation ratios across N in \[5, 8, 10, 12, 15, 18, 20, 30, 50\].  
4. Support random 2D Euclidean coordinate graphs and TSPLIB `.tsp` file parsing.  
5. Create visualization tools using Matplotlib to plot 2D tour paths and log-scale performance curves.  
6. Build a lightweight Streamlit dashboard (`src/app.py`) for interactive viva demonstrations.  
7. Write unit tests verifying tour correctness and run the entire suite.

