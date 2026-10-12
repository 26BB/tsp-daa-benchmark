import numpy as np
from typing import List, Tuple, Dict, Any
from src.algorithms.base import TSPSolver

class NearestNeighbour2OptSolver(TSPSolver):
    """
    Heuristic TSP Solver: Greedy Nearest Neighbour followed by 2-Opt Local Search.
    Time Complexity: O(n^2) construction + O(k * n^2) 2-opt swaps
    Space Complexity: O(n)
    
    1. Construction: Builds initial tour greedily by always visiting the closest unvisited city.
    2. Local Optimization (2-Opt): Iteratively cuts two intersecting edges and reconnects
       the endpoints backwards if it shortens total tour length. Terminates when local optimum is reached.
    """

    def __init__(self, max_iterations: int = 1000):
        super().__init__("Nearest Neighbour + 2-Opt")
        self.max_iterations = max_iterations

    def _nearest_neighbour(self, dist_matrix: np.ndarray, start: int = 0) -> List[int]:
        n = len(dist_matrix)
        visited = [False] * n
        tour = [start]
        visited[start] = True

        for _ in range(n - 1):
            curr = tour[-1]
            next_city = -1
            min_dist = float('inf')

            for j in range(n):
                if not visited[j] and dist_matrix[curr][j] < min_dist:
                    min_dist = dist_matrix[curr][j]
                    next_city = j

            visited[next_city] = True
            tour.append(next_city)

        tour.append(start)
        return tour

    def _two_opt_swap(self, tour: List[int], i: int, k: int) -> List[int]:
        """Reverses the path between index i and k: tour[0:i] + tour[i:k+1][::-1] + tour[k+1:]"""
        return tour[:i] + tour[i:k + 1][::-1] + tour[k + 1:]

    def solve(self, dist_matrix: np.ndarray) -> Tuple[float, List[int], Dict[str, Any]]:
        n = len(dist_matrix)
        if n <= 1:
            return 0.0, [0, 0] if n == 1 else [], {}
        if n == 2:
            cost = float(dist_matrix[0][1] + dist_matrix[1][0])
            return cost, [0, 1, 0], {}

        # 1. Greedy construction
        tour = self._nearest_neighbour(dist_matrix, start=0)
        best_cost = self.calculate_tour_cost(tour, dist_matrix)

        # 2. 2-Opt Iterative Improvement
        improved = True
        iterations = 0
        swaps_performed = 0

        while improved and iterations < self.max_iterations:
            improved = False
            iterations += 1

            for i in range(1, n - 1):
                for k in range(i + 1, n):
                    # Cost difference of swapping edge (i-1, i) and (k, k+1) with (i-1, k) and (i, k+1)
                    a, b = tour[i - 1], tour[i]
                    c, d = tour[k], tour[k + 1]

                    current_edge_cost = dist_matrix[a][b] + dist_matrix[c][d]
                    new_edge_cost = dist_matrix[a][c] + dist_matrix[b][d]

                    if new_edge_cost < current_edge_cost - 1e-9:
                        tour = self._two_opt_swap(tour, i, k)
                        best_cost += (new_edge_cost - current_edge_cost)
                        swaps_performed += 1
                        improved = True
                        break  # Move to next improvement cycle
                if improved:
                    break

        actual_cost = self.calculate_tour_cost(tour, dist_matrix)
        stats = {
            "iterations": iterations,
            "swaps_performed": swaps_performed,
            "algorithm": self.name
        }

        return float(actual_cost), tour, stats
