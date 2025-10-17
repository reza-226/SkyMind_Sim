# FILE: skymind_sim/layer_1_simulation/world/obstacle.py
from typing import List, Tuple

class Obstacle:
    """Represents a collection of grid cells that are impassable."""
    
    def __init__(self, positions: List[Tuple[int, int]]):
        """
        Initializes an obstacle with a list of grid coordinates it occupies.

        Args:
            positions (List[Tuple[int, int]]): A list of (x, y) tuples representing
                                               the grid cells occupied by the obstacle.
        """
        # A list of (x, y) tuples for each cell the obstacle occupies
        self.positions: List[Tuple[int, int]] = positions

    def get_positions(self) -> List[Tuple[int, int]]:
        """Returns the list of grid positions occupied by the obstacle."""
        return self.positions

    def __repr__(self):
        return f"Obstacle(positions={self.positions})"
