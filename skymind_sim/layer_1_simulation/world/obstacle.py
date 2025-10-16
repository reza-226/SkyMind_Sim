# Path: skymind_sim/layer_1_simulation/world/obstacle.py

from typing import Tuple

class Obstacle:
    """
    Represents a single, static obstacle in the simulation world.
    In a grid-based world, an obstacle occupies one or more cells.
    For simplicity, we assume each obstacle occupies exactly one cell.
    """
    def __init__(self, position: Tuple[int, int]):
        """
        Initializes an obstacle at a specific grid position.

        Args:
            position (Tuple[int, int]): The (x, y) coordinates of the obstacle on the grid.
        """
        if not isinstance(position, tuple) or len(position) != 2:
            raise ValueError("Position must be a tuple of two integers (x, y).")
        
        self._position = position

    def get_position(self) -> Tuple[int, int]:
        """
        Returns the position of the obstacle.

        Returns:
            Tuple[int, int]: The (x, y) coordinates of the obstacle.
        """
        return self._position

    def __repr__(self) -> str:
        """
        Provides a developer-friendly string representation of the obstacle.
        """
        return f"Obstacle(position={self._position})"
