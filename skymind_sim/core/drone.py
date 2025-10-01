# FILE: skymind_sim/core/drone.py

import numpy as np
import random

class Drone:
    """
    Represents a single drone in the simulation.
    It manages its own state, including position, velocity, and battery.
    """
    def __init__(self, drone_id, name="DefaultDrone", position=None, mass=1.0):
        """
        Initializes a Drone object.

        Args:
            drone_id (int): The unique identifier for the drone.
            name (str): The name of the drone.
            position (list, optional): Initial [x, y] position. Defaults to a random position.
            mass (float, optional): Mass of the drone in kg. Defaults to 1.0.
        """
        self.id = drone_id  # Use the provided drone_id as the main identifier
        self.name = name
        
        # If no position is provided, set a default.
        # Note: It's better to provide a position from the Environment class.
        if position is None:
            self.position = np.array([0.0, 0.0])
        else:
            self.position = np.array(position, dtype=float)
            
        self.velocity = np.array([random.uniform(-1, 1), random.uniform(-1, 1)], dtype=float)
        self.mass = mass
        self.max_speed = 5.0  # Maximum speed in units per second

    def update_state(self, world_width, world_height):
        """
        Updates the drone's position based on its velocity and handles boundary collision.
        """
        self.position += self.velocity

        # Simple wall bouncing logic
        if self.position[0] <= 0 or self.position[0] >= world_width:
            self.velocity[0] *= -1
        if self.position[1] <= 0 or self.position[1] >= world_height:
            self.velocity[1] *= -1
            
        # Clamp position to be within bounds to prevent getting stuck
        self.position[0] = np.clip(self.position[0], 0, world_width)
        self.position[1] = np.clip(self.position[1], 0, world_height)


    def get_bearing_degrees(self):
        """
        Calculates the drone's direction of travel (bearing) in degrees.
        0 degrees is East (right), 90 is North (up), 180 is West (left), 270 is South (down).
        """
        if np.linalg.norm(self.velocity) < 1e-6:
            return 0.0  # If not moving, default to 0 degrees
        angle_rad = np.arctan2(-self.velocity[1], self.velocity[0])
        angle_deg = np.degrees(angle_rad)
        return angle_deg

    def __str__(self):
        return (f"Drone(ID={self.id}, Name={self.name}, "
                f"Position=[{self.position[0]:.2f}, {self.position[1]:.2f}])")
