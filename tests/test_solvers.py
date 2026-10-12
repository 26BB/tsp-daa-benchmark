import pytest
import numpy as np
from src.core.graph import TSPGraph
from src.algorithms.exact_held_karp import HeldKarpSolver
from src.algorithms.exact_branch_bound import BranchAndBoundSolver
from src.algorithms.approx_mst_2approx import MST2ApproxSolver
from src.algorithms.heuristic_2opt import NearestNeighbour2OptSolver

@pytest.fixture
def sample_graph():
    # 5-city simple Euclidean graph
    coords = np.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [1.0, 1.0],
        [0.0, 1.0],
        [0.5, 0.5]
    ])
    return TSPGraph(name="Square5", coordinates=coords)

def test_graph_properties(sample_graph):
    assert sample_graph.n == 5
    assert sample_graph.dist_matrix.shape == (5, 5)
    # Distance between (0,0) and (1,0) should be 1.0
    assert np.isclose(sample_graph.dist_matrix[0][1], 1.0)
    # Diagonal should be 0
    assert np.isclose(sample_graph.dist_matrix[0][0], 0.0)

def test_held_karp_solver(sample_graph):
    solver = HeldKarpSolver()
    cost, tour, stats = solver.solve(sample_graph.dist_matrix)
    assert solver.is_valid_tour(tour, sample_graph.n)
    assert cost > 0.0

def test_branch_and_bound_solver(sample_graph):
    solver = BranchAndBoundSolver()
    cost, tour, stats = solver.solve(sample_graph.dist_matrix)
    assert solver.is_valid_tour(tour, sample_graph.n)
    assert cost > 0.0

def test_mst_2approx_solver(sample_graph):
    solver = MST2ApproxSolver()
    cost, tour, stats = solver.solve(sample_graph.dist_matrix)
    assert solver.is_valid_tour(tour, sample_graph.n)
    assert cost > 0.0

def test_2opt_solver(sample_graph):
    solver = NearestNeighbour2OptSolver()
    cost, tour, stats = solver.solve(sample_graph.dist_matrix)
    assert solver.is_valid_tour(tour, sample_graph.n)
    assert cost > 0.0

def test_exact_agreement_on_small_graph(sample_graph):
    hk = HeldKarpSolver()
    bb = BranchAndBoundSolver()
    cost_hk, tour_hk, _ = hk.solve(sample_graph.dist_matrix)
    cost_bb, tour_bb, _ = bb.solve(sample_graph.dist_matrix)
    # Both exact algorithms should return identical optimal costs
    assert np.isclose(cost_hk, cost_bb, atol=1e-3)

def test_2approx_bound(sample_graph):
    hk = HeldKarpSolver()
    mst = MST2ApproxSolver()
    cost_opt, _, _ = hk.solve(sample_graph.dist_matrix)
    cost_approx, _, _ = mst.solve(sample_graph.dist_matrix)
    # Cost should strictly satisfy cost_approx <= 2 * cost_opt
    assert cost_approx <= 2.0 * cost_opt + 1e-6
