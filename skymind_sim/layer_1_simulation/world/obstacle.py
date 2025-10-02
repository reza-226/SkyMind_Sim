# skymind_sim/layer_1_simulation/world/obstacle.py

from typing import Tuple

class Obstacle:
    """
    Represents a static obstacle in the simulation world.
    This is part of Layer 1 as it's a fundamental component of the simulation environment.
    """
    def __init__(self, obstacle_id: int, position: Tuple[float, float], size: Tuple[float, float]):
        """
        Initializes an Obstacle instance.

        Args:
            obstacle_id (int): A unique identifier for the obstacle.
            position (Tuple[float, float]): The (x, y) coordinates of the top-left corner.
            size (Tuple[float, float]): The (width, height) of the obstacle.
        """
        self.id = obstacle_id
        self.position = position
        self.size = size
        print(f"Obstacle {self.id} created at {self.position} with size {self.size}.")

    def get_state(self) -> dict:
        """
        Returns the state of the obstacle for rendering or collision detection.
        """
        return {
            'id': self.id,
            'position': self.position,
            'size': self.size,
        }
