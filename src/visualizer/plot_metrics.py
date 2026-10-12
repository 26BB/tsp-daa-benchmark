import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional

def plot_runtime_scaling(df: pd.DataFrame, save_path: Optional[str] = None):
    """
    Plots log-scale Execution Time vs. Number of Cities (N) for all algorithms.
    Illustrates the exponential barrier of exact methods vs polynomial heuristics.
    """
    fig, ax = plt.subplots(figsize=(9, 6))

    # Filter out errored rows
    valid_df = df[df["time_sec"].notna() & (df["time_sec"] > 0)]

    for algo, group in valid_df.groupby("algorithm"):
        sorted_group = group.sort_values("n_cities")
        ax.plot(
            sorted_group["n_cities"], 
            sorted_group["time_sec"], 
            marker='o', 
            linewidth=2, 
            label=algo
        )

    ax.set_yscale('log')
    ax.set_title("Computational Complexity Scaling (Log-Scale Time vs. N)", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Number of Cities (N)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Execution Time (seconds, log scale)", fontsize=11, fontweight='bold')
    ax.legend(title="Algorithm", loc="upper left", frameon=True)
    ax.grid(True, which="both", ls="--", alpha=0.5)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    return fig

def plot_cost_comparison(df: pd.DataFrame, save_path: Optional[str] = None):
    """
    Plots Tour Cost vs. Number of Cities (N) to visualize solution quality and approximation accuracy.
    """
    fig, ax = plt.subplots(figsize=(9, 6))
    valid_df = df[df["cost"].notna()]

    for algo, group in valid_df.groupby("algorithm"):
        sorted_group = group.sort_values("n_cities")
        ax.plot(
            sorted_group["n_cities"], 
            sorted_group["cost"], 
            marker='s', 
            linewidth=2, 
            label=algo
        )

    ax.set_title("Solution Quality Comparison (Tour Cost vs. N)", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Number of Cities (N)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Total Tour Length / Cost", fontsize=11, fontweight='bold')
    ax.legend(title="Algorithm", loc="upper left", frameon=True)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    return fig
