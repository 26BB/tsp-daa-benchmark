import numpy as np
from typing import List, Tuple, Dict, Any
from collections import defaultdict
from src.algorithms.base import TSPSolver

class MST2ApproxSolver(TSPSolver):
    """
    2-Approximation Algorithm for Metric TSP via Minimum Spanning Tree (MST).
    Theoretical Time Complexity: O(n^2)
    Space Complexity: O(n)
    
    Steps:
    1. Compute MST using Prim's algorithm on the Euclidean distance matrix.
    2. Perform a Depth-First Search (DFS) / Preorder traversal on the MST.
    3. Take 'shortcuts' bypassing already visited cities (justified by Triangle Inequality: c(u, w) <= c(u, v) + c(v, w)).
    4. Theoretical guarantee: Cost(Tour) <= 2 * Cost(Optimal Tour).
    """

    def __init__(self):
        super().__init__("MST 2-Approximation")

    def _prims_mst(self, dist_matrix: np.ndarray) -> Dict[int, List[int]]:
        """Computes MST using Prim's algorithm in O(n^2)."""
        n = len(dist_matrix)
        visited = [False] * n
        min_weight = [float('inf')] * n
        parent = [-1] * n

        # Start from node 0
        min_weight[0] = 0.0

        for _ in range(n):
            # Pick minimum weight unvisited vertex
            u = -1
            for i in range(n):
                if not visited[i] and (u == -1 or min_weight[i] < min_weight[u]):
                    u = i

            visited[u] = True

            # Update adjacent weights
            for v in range(n):
                if not visited[v] and dist_matrix[u][v] < min_weight[v]:
                    min_weight[v] = dist_matrix[u][v]
                    parent[v] = u

        # Build adjacency list for tree
        adj: Dict[int, List[int]] = defaultdict(list)
        for v in range(1, n):
            p = parent[v]
            adj[p].append(v)
            adj[v].append(p)
            
        return adj

    def solve(self, dist_matrix: np.ndarray) -> Tuple[float, List[int], Dict[str, Any]]:
        n = len(dist_matrix)
        if n <= 1:
            return 0.0, [0, 0] if n == 1 else [], {}
        if n == 2:
            cost = float(dist_matrix[0][1] + dist_matrix[1][0])
            return cost, [0, 1, 0], {}

        # 1. Compute MST
        mst_adj = self._prims_mst(dist_matrix)

        # 2. Preorder DFS Traversal with Shortcuts
        visited_nodes = [False] * n
        tour_order: List[int] = []

        def dfs(u: int):
            visited_nodes[u] = True
            tour_order.append(u)
            for neighbor in mst_adj[u]:
                if not visited_nodes[neighbor]:
                    dfs(neighbor)

        dfs(0)

        # 3. Complete the cycle by returning to start
        full_tour = tour_order + [tour_order[0]]
        total_cost = self.calculate_tour_cost(full_tour, dist_matrix)

        stats = {
            "mst_edges": n - 1,
            "algorithm": self.name
        }

        return float(total_cost), full_tour, stats
