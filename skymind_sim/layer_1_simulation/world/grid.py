# Path: skymind_sim/layer_1_simulation/world/grid.py

from typing import Tuple, List, Set
from skymind_sim.utils.log_manager import LogManager

class Grid:
    """
    Represents the 2D grid world of the simulation. It stores dimensions
    and the locations of obstacles.
    """
    def __init__(self, width: int, height: int):
        """
        Initializes the grid.

        Args:
            width (int): The number of cells in the x-direction.
            height (int): The number of cells in the y-direction.
        """
        self.logger = LogManager.get_logger(__name__)
        self.width = width
        self.height = height
        # Using a set for efficient checking of obstacle presence (O(1) average time complexity)
        self._obstacle_positions: Set[Tuple[int, int]] = set()

    def get_dimensions(self) -> Tuple[int, int]:
        """
        Returns the width and height of the grid.

        Returns:
            Tuple[int, int]: A tuple containing (width, height).
        """
        return self.width, self.height

    def is_obstacle(self, position: Tuple[int, int]) -> bool:
        """
        Checks if a cell at a given position contains an obstacle.

        Args:
            position (Tuple[int, int]): The (x, y) coordinates to check.

        Returns:
            bool: True if the cell has an obstacle, False otherwise.
        """
        return position in self._obstacle_positions

    def add_obstacle(self, position: Tuple[int, int]):
        """
        Adds an obstacle at a given position.

        Args:
            position (Tuple[int, int]): The (x, y) coordinates of the obstacle.
        """
        if 0 <= position[0] < self.width and 0 <= position[1] < self.height:
            self._obstacle_positions.add(position)
        else:
            self.logger.warning(f"Attempted to add obstacle at out-of-bounds position: {position}")


    def get_obstacles(self) -> List[Tuple[int, int]]:
        """
        Returns a list of all obstacle positions.

        Returns:
            List[Tuple[int, int]]: A list of (x, y) tuples for each obstacle.
        """
        return list(self._obstacle_positions)
