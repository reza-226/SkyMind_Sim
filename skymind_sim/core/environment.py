# skymind_sim/core/environment.py

import numpy as np

class Environment:
    """
    Represents the simulation environment, including its boundaries and the drones within it.
    """

    def __init__(self, width: float, height: float, depth: float = 100.0):
        if width <= 0 or height <= 0 or depth <= 0:
            raise ValueError("Environment dimensions (width, height, depth) must be positive.")
        
        self.width = width
        self.height = height
        self.depth = depth
        self.drones = {}  # Using a dictionary is better for lookups by ID

    def add_drone(self, drone):
        """Adds a drone to the environment, checking its initial position."""
        if drone.id in self.drones:
            raise ValueError(f"Drone with ID {drone.id} already exists.")

        pos = drone.position
        if not (0 <= pos[0] <= self.width and 0 <= pos[1] <= self.height and 0 <= pos[2] <= self.depth):
            raise ValueError(f"Drone {drone.id} initial position {pos} is outside the environment boundaries.")

        self.drones[drone.id] = drone

    def get_drone(self, drone_id: int):
        """Retrieves a drone by its ID."""
        return self.drones.get(drone_id)

    def get_drones(self):
        """Returns a list of all drone objects in the environment."""
        return list(self.drones.values())

    @property
    def drones_count(self):
        """Returns the number of drones in the environment."""
        return len(self.drones)

    def __repr__(self):
        """Provides a developer-friendly representation of the environment."""
        return f"Environment(width={self.width}, height={self.height}, depth={self.depth}, drones_count={self.drones_count})"
