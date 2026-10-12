import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional
from src.core.graph import TSPGraph

def plot_tour(graph: TSPGraph, tour: List[int], title: str = "TSP Tour", 
              cost: Optional[float] = None, save_path: Optional[str] = None):
    """
    Renders 2D scatter plot of cities and draws the closed tour cycle.
    """
    coords = graph.coordinates
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot cities
    ax.scatter(coords[:, 0], coords[:, 1], c='crimson', s=60, zorder=5, label="Cities")

    # Annotate city numbers
    for idx, (x, y) in enumerate(coords):
        ax.annotate(str(idx), (x, y), textcoords="offset points", xytext=(0, 6),
                    ha='center', fontsize=9, fontweight='bold', color='navy')

    # Draw tour edges
    if tour and len(tour) > 1:
        tour_coords = coords[tour]
        ax.plot(tour_coords[:, 0], tour_coords[:, 1], c='royalblue', linewidth=1.8, 
                linestyle='-', zorder=3, label="Tour Path")
        # Highlight start node
        start_x, start_y = coords[tour[0]]
        ax.scatter([start_x], [start_y], c='forestgreen', s=120, edgecolors='black', 
                   linewidth=2, zorder=6, label="Start City")

    title_text = title
    if cost is not None:
        title_text += f" (Cost: {cost:.2f})"
    ax.set_title(title_text, fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.legend(loc='best', frameon=True)
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    return fig
