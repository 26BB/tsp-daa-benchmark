from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any
import numpy as np

class TSPSolver(ABC):
    """
    Abstract Base Class for TSP Solvers.
    Every solver takes a distance matrix and returns:
    - best_cost (float): Total length of the tour.
    - tour (List[int]): Ordered sequence of visited vertex indices, returning to start.
    - stats (Dict[str, Any]): Additional solver metrics (e.g., iterations, nodes pruned).
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def solve(self, dist_matrix: np.ndarray) -> Tuple[float, List[int], Dict[str, Any]]:
        """
        Solves the TSP for the given symmetric distance matrix.
        
        Args:
            dist_matrix (np.ndarray): N x N distance matrix where dist_matrix[i][j] is the distance from i to j.
            
        Returns:
            Tuple[float, List[int], Dict[str, Any]]:
                - best_cost: Length of optimal/approximated cycle.
                - tour: List of node indices representing the cycle (e.g., [0, 2, 1, 3, 0]).
                - stats: Dictionary with extra info.
        """
        pass

    @staticmethod
    def calculate_tour_cost(tour: List[int], dist_matrix: np.ndarray) -> float:
        """Helper to calculate the total length of a tour."""
        cost = 0.0
        for i in range(len(tour) - 1):
            cost += dist_matrix[tour[i]][tour[i + 1]]
        return float(cost)

    @staticmethod
    def is_valid_tour(tour: List[int], n: int) -> bool:
        """Validates that every vertex from 0 to n-1 is visited exactly once and returns to start."""
        if len(tour) != n + 1:
            return False
        if tour[0] != tour[-1]:
            return False
        return sorted(tour[:-1]) == list(range(n))
