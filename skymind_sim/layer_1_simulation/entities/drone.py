# skymind_sim/layer_1_simulation/entities/drone.py

from typing import Tuple

class Drone:
    """
    Represents a single drone in the simulation.
    It holds the drone's state, such as position, battery, etc.
    This class belongs to Layer 1 (Simulation) as it's a core entity of the simulation world.
    """
    def __init__(self, drone_id: int, position: Tuple[float, float]):
        """
        Initializes a Drone instance.

        Args:
            drone_id (int): A unique identifier for the drone.
            position (Tuple[float, float]): The initial (x, y) coordinates of the drone.
        """
        self.id = drone_id
        self.position = position
        print(f"Drone {self.id} created at position {self.position}.")

    def move(self, dx: float, dy: float):
        """
        Updates the drone's position by a given delta.
        
        Args:
            dx (float): Change in the x-coordinate.
            dy (float): Change in the y-coordinate.
        """
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy
        self.position = (new_x, new_y)
        print(f"Drone {self.id} moved to {self.position}.")

    def get_state(self) -> dict:
        """
        Returns the current state of the drone.
        Useful for rendering (Layer 0) or decision making (Layer 3).
        """
        return {
            'id': self.id,
            'position': self.position,
        }

    def __str__(self) -> str:
        return f"Drone(ID={self.id}, Position={self.position})"
