# skymind_sim/core/environment.py

import numpy as np

class Environment:
    """
    Represents the 3D simulation environment, including its dimensions and the drones within it.
    """
    def __init__(self, width: float, height: float, depth: float):
        """
        Initializes the environment.

        Args:
            width (float): The width of the environment (X-axis).
            height (float): The height of the environment (Y-axis).
            depth (float): The depth of the environment (Z-axis).
        """
        self.dimensions = np.array([width, height, depth])
        self.drones = []  # This will store Drone objects

    def add_drone(self, drone):
        """
        Adds a single drone object to the environment's list of drones.

        Args:
            drone (Drone): The drone object to add.
        """
        # Fix: Append the entire drone object, not just its ID.
        self.drones.append(drone)

    def get_drone(self, drone_id: int):
        """
        Finds and returns a drone by its ID.

        Args:
            drone_id (int): The ID of the drone to find.

        Returns:
            Drone: The drone object if found, otherwise None.
        """
        for drone in self.drones:
            if drone.drone_id == drone_id:
                return drone
        return None
