import heapq
import numpy as np
from typing import List, Tuple, Dict, Any
from src.algorithms.base import TSPSolver

class BranchAndBoundSolver(TSPSolver):
    """
    Exact TSP Solver using Branch and Bound with Reduced Cost Matrix (RCM).
    Time Complexity: Worst-case O(n!), pruned average case
    Space Complexity: O(n^2 * state_tree_depth)
    
    Standard textbook formulation (Horowitz-Sahni / Cormen):
    At each state:
    1. A reduced cost matrix maintains lower bounds.
    2. Branching from current node i to next node j:
       child_bound = parent_bound + parent_matrix[i, j] + r_cost(child_matrix)
    3. In child matrix, row i is set to inf, col j is set to inf, and matrix[j, 0] is set to inf
       (to prevent premature sub-tour before all vertices visited).
    """

    def __init__(self, max_states: int = 50_000):
        super().__init__("Branch & Bound (RCM)")
        self.max_states = max_states

    @staticmethod
    def _reduce_matrix(matrix: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Reduces rows and columns of matrix by subtracting minimums.
        Returns reduced matrix and total reduction cost.
        """
        n = matrix.shape[0]
        reduced = matrix.copy()
        reduction_cost = 0.0

        # Row reduction
        for i in range(n):
            row = reduced[i, :]
            finite = row[row < float('inf')]
            if len(finite) > 0:
                m = np.min(finite)
                if m > 0 and m < float('inf'):
                    reduced[i, :] -= m
                    reduction_cost += m

        # Column reduction
        for j in range(n):
            col = reduced[:, j]
            finite = col[col < float('inf')]
            if len(finite) > 0:
                m = np.min(finite)
                if m > 0 and m < float('inf'):
                    reduced[:, j] -= m
                    reduction_cost += m

        return reduced, float(reduction_cost)

    def solve(self, dist_matrix: np.ndarray) -> Tuple[float, List[int], Dict[str, Any]]:
        n = len(dist_matrix)
        if n <= 1:
            return 0.0, [0, 0] if n == 1 else [], {"explored_nodes": 0}
        if n == 2:
            cost = float(dist_matrix[0][1] + dist_matrix[1][0])
            return cost, [0, 1, 0], {"explored_nodes": 1}

        # Initialize with infinity on diagonal
        init_mat = dist_matrix.astype(float).copy()
        np.fill_diagonal(init_mat, float('inf'))

        # Root reduction
        root_mat, root_bound = self._reduce_matrix(init_mat)

        # Get an initial upper bound from Nearest Neighbour heuristic to prune aggressively early
        curr = 0
        nn_tour = [0]
        visited = {0}
        for _ in range(n - 1):
            next_c = min((c for c in range(n) if c not in visited), key=lambda c: dist_matrix[curr, c])
            nn_tour.append(next_c)
            visited.add(next_c)
            curr = next_c
        nn_tour.append(0)
        best_cost = self.calculate_tour_cost(nn_tour, dist_matrix)
        best_tour = nn_tour

        # Priority Queue entries: (lower_bound, level, counter, curr_node, path, matrix)
        counter = 0
        pq = [(root_bound, 1, counter, 0, [0], root_mat)]
        explored_nodes = 0
        pruned_nodes = 0

        while pq and explored_nodes < self.max_states:
            bound, level, _, curr_node, path, curr_mat = heapq.heappop(pq)
            explored_nodes += 1

            if bound >= best_cost:
                pruned_nodes += 1
                continue

            # Leaf reached: all n nodes in path
            if level == n:
                # Return to start node 0
                tour_candidate = path + [0]
                actual_cost = self.calculate_tour_cost(tour_candidate, dist_matrix)
                if actual_cost < best_cost:
                    best_cost = actual_cost
                    best_tour = tour_candidate
                continue

            # Branch to unvisited cities
            visited_set = set(path)
            for next_node in range(n):
                if next_node not in visited_set and curr_mat[curr_node, next_node] < float('inf'):
                    edge_val = curr_mat[curr_node, next_node]

                    child_mat = curr_mat.copy()
                    child_mat[curr_node, :] = float('inf')
                    child_mat[:, next_node] = float('inf')
                    # Block return to start until the last step
                    if level < n - 1:
                        child_mat[next_node, 0] = float('inf')

                    reduced_child, child_reduction = self._reduce_matrix(child_mat)
                    child_bound = bound + edge_val + child_reduction

                    if child_bound < best_cost:
                        counter += 1
                        heapq.heappush(
                            pq,
                            (child_bound, level + 1, counter, next_node, path + [next_node], reduced_child)
                        )
                    else:
                        pruned_nodes += 1

        stats = {
            "explored_nodes": explored_nodes,
            "pruned_nodes": pruned_nodes,
            "algorithm": self.name
        }
        return float(best_cost), best_tour, stats
