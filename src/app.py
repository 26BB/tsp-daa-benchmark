import streamlit as st
import numpy as np
import pandas as pd
import time
import os

from src.core.graph import TSPGraph
from src.core.benchmark import TSPBenchmark
from src.algorithms.exact_held_karp import HeldKarpSolver
from src.algorithms.exact_branch_bound import BranchAndBoundSolver
from src.algorithms.approx_mst_2approx import MST2ApproxSolver
from src.algorithms.heuristic_2opt import NearestNeighbour2OptSolver
from src.visualizer.plot_tours import plot_tour
from src.visualizer.plot_metrics import plot_runtime_scaling, plot_cost_comparison

st.set_page_config(
    page_title="DAA Mini Project - TSP Exact vs Approximation",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Travelling Salesperson Problem (TSP): Exact vs Approximation")
st.markdown("""
**Course:** Design and Analysis of Algorithms (DAA) — BE Computer Engineering  
**Objective:** Compare exact exponential algorithms against polynomial-time approximation and heuristic strategies across solution quality, execution time, and memory overhead.
""")

st.sidebar.header("⚙️ Experiment Controls")
input_mode = st.sidebar.radio("Data Source:", ["Random 2D Euclidean Graph", "TSPLIB Benchmark File"])

if input_mode == "Random 2D Euclidean Graph":
    n_cities = st.sidebar.slider("Number of Cities (N):", min_value=4, max_value=50, value=10, step=1)
    seed = st.sidebar.number_input("Random Seed:", min_value=0, max_value=9999, value=42)
    graph = TSPGraph.generate_random(n_cities, seed=seed)
else:
    tsplib_file = st.sidebar.selectbox("Choose TSPLIB Instance:", ["data/sample_tsplib/eil51.tsp"])
    if os.path.exists(tsplib_file):
        graph = TSPGraph.from_tsplib(tsplib_file)
        n_cities = graph.n
        st.sidebar.info(f"Loaded {graph.name} with {n_cities} cities.")
    else:
        st.sidebar.error("TSPLIB file not found.")
        st.stop()

# Algorithm selection
st.sidebar.subheader("Algorithms to Run")
run_hk = st.sidebar.checkbox("Held-Karp DP (Exact)", value=(n_cities <= 14))
run_bb = st.sidebar.checkbox("Branch & Bound (RCM)", value=(n_cities <= 14))
run_mst = st.sidebar.checkbox("MST 2-Approximation", value=True)
run_2opt = st.sidebar.checkbox("Nearest Neighbour + 2-Opt", value=True)

if n_cities > 16 and (run_hk or run_bb):
    st.sidebar.warning("⚠️ Warning: Exact algorithms (Held-Karp & B&B) have exponential complexity O(2^n / n!). Running them for N > 16 may cause high latency.")

run_btn = st.button("🚀 Run Solvers & Compare", type="primary")

if run_btn:
    solvers = []
    if run_hk:
        solvers.append(HeldKarpSolver())
    if run_bb:
        solvers.append(BranchAndBoundSolver())
    if run_mst:
        solvers.append(MST2ApproxSolver())
    if run_2opt:
        solvers.append(NearestNeighbour2OptSolver())

    if not solvers:
        st.warning("Please select at least one algorithm.")
        st.stop()

    benchmark = TSPBenchmark(solvers)
    results = []
    tours = {}

    with st.spinner("Executing solvers and recording metrics..."):
        for solver in solvers:
            res = benchmark.benchmark_single(solver, graph)
            results.append(res)
            tours[solver.name] = (res["cost"], res["tour"])

    df = pd.DataFrame(results)

    # Compute approx ratio
    optimal_cost = None
    if run_hk and not df[df["algorithm"] == "Held-Karp (Exact DP)"].empty:
        optimal_cost = df[df["algorithm"] == "Held-Karp (Exact DP)"]["cost"].values[0]
    else:
        optimal_cost = df["cost"].min()

    df["approx_ratio"] = df["cost"].apply(lambda c: round(c / optimal_cost, 3) if optimal_cost else 1.0)

    # Display Metrics Table
    st.subheader("📊 Comparative Evaluation Table")
    display_df = df[["algorithm", "cost", "approx_ratio", "time_sec", "peak_memory_kb", "is_valid"]].copy()
    display_df.columns = ["Algorithm", "Tour Cost", "Approx Ratio (Cost / Opt)", "Execution Time (s)", "Peak RAM (KB)", "Valid Tour?"]
    st.dataframe(display_df, use_container_width=True)

    # Tour Visualizations Side-by-Side
    st.subheader("📍 Visual Tour Routes")
    cols = st.columns(min(len(solvers), 2))
    for idx, (algo_name, (cost, tour)) in enumerate(tours.items()):
        col = cols[idx % 2]
        with col:
            fig = plot_tour(graph, tour, title=algo_name, cost=cost)
            st.pyplot(fig)

    # Viva / Academic Notes
    st.subheader("💡 Academic & Viva Insights")
    st.markdown("""
    - **Held-Karp Dynamic Programming:** Guarantees optimal tour using subproblem memoization ($O(n^2 2^n)$), but memory and runtime scale exponentially.
    - **Branch and Bound:** Prunes search branches using the Reduced Cost Matrix lower bound, dramatically reducing explored state count compared to brute-force $O(n!)$.
    - **MST 2-Approximation:** Explores Minimum Spanning Tree preorder shortcuts. Provably bounded such that $\\text{Cost} \\le 2 \\times \\text{Optimal}$.
    - **Nearest Neighbour + 2-Opt:** Polynomial heuristic ($O(n^2)$) that removes intersecting edges to deliver near-optimal solutions in milliseconds.
    """)
