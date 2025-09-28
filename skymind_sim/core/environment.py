# skymind_sim/core/environment.py (نسخه اصلاح شده)

from typing import List
from .drone import Drone

class Environment:
    def __init__(self, width: float, height: float):
        if not (width > 0 and height > 0):
            raise ValueError("Environment dimensions must be positive.")
        self.width = width
        self.height = height
        self.drones: List[Drone] = []

    def add_drone(self, drone: Drone):
        """
        Adds a drone to the environment.

        Args:
            drone (Drone): The drone instance to be added.
        """
        if not (0 <= drone.position[0] < self.width and 0 <= drone.position[1] < self.height):
            # *** تغییر در این خط ***
            raise ValueError(f"Drone with ID {drone.id} is outside the environment boundaries.")
        
        self.drones.append(drone)

    def __repr__(self) -> str:
        return f"Environment(width={self.width}, height={self.height}, drones_count={len(self.drones)})"
