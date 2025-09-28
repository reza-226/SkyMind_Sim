# skymind_sim/core/drone.py

import numpy as np
from enum import Enum, auto

class DroneStatus(Enum):
    """Enumeration for drone status."""
    IDLE = auto()
    FLYING = auto()
    LANDING = auto()
    CHARGING = auto()
    ERROR = auto()
    
    # This makes sure that when we convert it to string (e.g., for JSON),
    # we get a clean string like "IDLE" instead of "DroneStatus.IDLE".
    def __str__(self):
        return self.name

class Drone:
    """Represents a single drone in the simulation."""

    def __init__(self, drone_id: int):
        if not isinstance(drone_id, int):
            raise TypeError("Drone ID must be an integer.")
        
        self.id = drone_id
        self.position = np.array([0.0, 0.0, 0.0])
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.status = DroneStatus.IDLE  # Default status

    def move_to(self, new_position: np.ndarray):
        """
        Updates the drone's position.
        
        Args:
            new_position (np.ndarray): The new 3D position vector.
        """
        if new_position.shape != (3,):
            raise ValueError("Position must be a 3D numpy array.")
        self.position = new_position

    def set_velocity(self, new_velocity: np.ndarray):
        """
        Updates the drone's velocity.
        
        Args:
            new_velocity (np.ndarray): The new 3D velocity vector.
        """
        if new_velocity.shape != (3,):
            raise ValueError("Velocity must be a 3D numpy array.")
        self.velocity = new_velocity

    def __repr__(self):
        """Provides a developer-friendly string representation of the drone."""
        pos = f"[{self.position[0]:.2f}, {self.position[1]:.2f}, {self.position[2]:.2f}]"
        return f"Drone(id={self.id}, status={self.status.name}, position={pos})"
