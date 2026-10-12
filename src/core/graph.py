import os
import math
import numpy as np
from typing import List, Tuple, Optional

class TSPGraph:
    """
    Graph representation for TSP instances:
    Supports 2D Euclidean coordinate sets and TSPLIB .tsp file parsing.
    """

    def __init__(self, name: str, coordinates: np.ndarray):
        self.name = name
        self.coordinates = coordinates  # N x 2 array of floats
        self.n = len(coordinates)
        self.dist_matrix = self._compute_distance_matrix()

    def _compute_distance_matrix(self) -> np.ndarray:
        """Computes symmetric Euclidean distance matrix."""
        diff = self.coordinates[:, np.newaxis, :] - self.coordinates[np.newaxis, :, :]
        return np.sqrt(np.sum(diff ** 2, axis=-1))

    @classmethod
    def generate_random(cls, n: int, seed: Optional[int] = 42, width: float = 1000.0, height: float = 1000.0) -> 'TSPGraph':
        """Generates random 2D points uniformly distributed in [0, width] x [0, height]."""
        if seed is not None:
            np.random.seed(seed)
        coords = np.random.uniform(0, max(width, height), size=(n, 2))
        return cls(name=f"Random-{n}", coordinates=coords)

    @classmethod
    def from_tsplib(cls, filepath: str) -> 'TSPGraph':
        """
        Parses TSPLIB formatted file (.tsp) with EUC_2D coordinates.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"TSPLIB file not found: {filepath}")

        coords = []
        name = os.path.splitext(os.path.basename(filepath))[0]
        in_coord_section = False

        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("NAME"):
                    parts = line.split(":")
                    if len(parts) > 1:
                        name = parts[1].strip()
                elif line == "NODE_COORD_SECTION":
                    in_coord_section = True
                    continue
                elif line == "EOF":
                    break
                elif in_coord_section:
                    parts = line.split()
                    if len(parts) >= 3:
                        # Format: <index> <x> <y>
                        x, y = float(parts[1]), float(parts[2])
                        coords.append([x, y])

        if not coords:
            raise ValueError(f"No coordinates found in TSPLIB file: {filepath}")

        return cls(name=name, coordinates=np.array(coords, dtype=float))
