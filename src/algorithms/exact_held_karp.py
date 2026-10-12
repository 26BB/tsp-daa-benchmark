import numpy as np
from typing import List, Tuple, Dict, Any
from src.algorithms.base import TSPSolver

class HeldKarpSolver(TSPSolver):
    """
    Exact TSP Solver using Held-Karp Dynamic Programming with Bitmasking.
    Time Complexity: O(n^2 * 2^n)
    Space Complexity: O(n * 2^n)
    
    dp[mask][u] stores the minimum cost of a path visiting all vertices in `mask` 
    starting from vertex 0 and ending at vertex `u`.
    """

    def __init__(self):
        super().__init__("Held-Karp (Exact DP)")

    def solve(self, dist_matrix: np.ndarray) -> Tuple[float, List[int], Dict[str, Any]]:
        n = len(dist_matrix)
        if n <= 1:
            return 0.0, [0, 0] if n == 1 else [], {"states_computed": 0}
        if n == 2:
            cost = float(dist_matrix[0][1] + dist_matrix[1][0])
            return cost, [0, 1, 0], {"states_computed": 1}

        # memo table: dp[mask][u] = (min_cost, parent)
        # mask is an integer where bit i is 1 if vertex i is visited.
        # We fix starting vertex as 0.
        memo: Dict[Tuple[int, int], Tuple[float, int]] = {}
        
        # Base cases: paths from 0 to u visiting only {0, u}
        for u in range(1, n):
            mask = (1 << 0) | (1 << u)
            memo[(mask, u)] = (float(dist_matrix[0][u]), 0)

        # Iterate over subset sizes from 3 to n
        # To compute systematically, we generate masks with increasing popcount
        for r in range(3, n + 1):
            for mask in range(1 << n):
                if not (mask & 1):  # Must include vertex 0
                    continue
                # Count set bits
                if bin(mask).count('1') != r:
                    continue

                for u in range(1, n):
                    if not (mask & (1 << u)):
                        continue
                    
                    prev_mask = mask ^ (1 << u)
                    best_cost = float('inf')
                    best_p = -1

                    for p in range(1, n):
                        if (prev_mask & (1 << p)) and (prev_mask, p) in memo:
                            cost = memo[(prev_mask, p)][0] + dist_matrix[p][u]
                            if cost < best_cost:
                                best_cost = cost
                                best_p = p
                    
                    if best_p != -1:
                        memo[(mask, u)] = (best_cost, best_p)

        # Connect back to start vertex 0
        all_visited_mask = (1 << n) - 1
        best_tour_cost = float('inf')
        last_node = -1

        for u in range(1, n):
            if (all_visited_mask, u) in memo:
                cost = memo[(all_visited_mask, u)][0] + dist_matrix[u][0]
                if cost < best_tour_cost:
                    best_tour_cost = cost
                    last_node = u

        # Reconstruct tour backwards
        tour = [0]
        curr_mask = all_visited_mask
        curr_node = last_node
        path = []

        while curr_node != 0 and curr_node != -1:
            path.append(curr_node)
            next_node = memo[(curr_mask, curr_node)][1]
            curr_mask = curr_mask ^ (1 << curr_node)
            curr_node = next_node

        tour.extend(reversed(path))
        tour.append(0)

        stats = {
            "states_computed": len(memo),
            "algorithm": self.name
        }

        return float(best_tour_cost), tour, stats
