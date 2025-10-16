# skymind_sim/layer_1_simulation/entities/drone.py

import random

class Drone:
    """
    Represents a drone in the simulation. It has a position and can move.
    """
    def __init__(self, drone_id: int, start_position: tuple[int, int]):
        """
        Initializes a Drone.
        
        Args:
            drone_id (int): A unique identifier for the drone.
            start_position (tuple[int, int]): The starting (x, y) grid coordinates.
        """
        self.drone_id = drone_id
        self.position = start_position
        
        # --- کدهای جدید ---
        self._move_timer = 0.0  # Timer to control movement speed
        self._move_interval = 0.5  # Move every 0.5 seconds

    def get_position(self) -> tuple[int, int]:
        """Returns the current (x, y) position of the drone."""
        return self.position

    def update(self, delta_time: float, grid_width: int, grid_height: int):
        """
        Updates the drone's state. For now, it handles simple random movement.
        
        Args:
            delta_time (float): The time elapsed since the last frame.
            grid_width (int): The width of the grid to stay within bounds.
            grid_height (int): The height of the grid to stay within bounds.
        """
        self._move_timer += delta_time
        if self._move_timer >= self._move_interval:
            self._move_timer = 0  # Reset timer
            self._perform_random_move(grid_width, grid_height)

    def _perform_random_move(self, grid_width: int, grid_height: int):
        """
        Calculates and applies a random one-step move (up, down, left, right).
        Ensures the drone stays within the grid boundaries.
        """
        possible_moves = [
            (0, 1),   # Down
            (0, -1),  # Up
            (1, 0),   # Right
            (-1, 0)   # Left
        ]
        
        dx, dy = random.choice(possible_moves)
        
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy

        # Check boundaries
        if 0 <= new_x < grid_width and 0 <= new_y < grid_height:
            self.position = (new_x, new_y)
            # Note: We are not checking for collisions with obstacles yet.
