# skymind_sim/core/drone.py

import numpy as np
from typing import List, Optional

class Drone:
    """
    Represents a single drone in the simulation.
    
    Manages its own state, including position, velocity, and mission waypoints.
    """
    def __init__(self,
                 id: str,
                 pos: np.ndarray,
                 waypoints: List[np.ndarray],
                 speed: float = 50.0,
                 waypoint_threshold: float = 5.0):
        """
        Initializes a Drone instance.

        Args:
            id (str): A unique identifier for the drone.
            pos (np.ndarray): The starting position of the drone as a 2D NumPy array [x, y].
            waypoints (List[np.ndarray]): A list of target coordinates (waypoints).
            speed (float): The cruising speed of the drone in units per second.
            waypoint_threshold (float): The distance at which a waypoint is considered "reached".
        """
        self.id = id
        self.pos = pos.astype(float) # Ensure position is float for precise calculations
        self.waypoints = [wp.astype(float) for wp in waypoints]
        self.speed = float(speed)
        self.waypoint_threshold = float(waypoint_threshold)

        self.current_waypoint_index = 0
        self.velocity = np.array([0.0, 0.0])
        self.mission_complete = False

        self._update_target()

    def _update_target(self):
        """Sets the velocity vector towards the current target waypoint."""
        if self.is_mission_complete():
            self.velocity = np.array([0.0, 0.0])
            return

        target_pos = self.waypoints[self.current_waypoint_index]
        direction_vector = target_pos - self.pos
        distance = np.linalg.norm(direction_vector)

        if distance > 0:
            self.velocity = (direction_vector / distance) * self.speed
        else:
            self.velocity = np.array([0.0, 0.0])

    def update(self, dt: float):
        """
        Updates the drone's state over a time step 'dt'.
        
        Args:
            dt (float): The time delta for this update step.
        """
        if self.is_mission_complete():
            return

        # Check if current waypoint is reached
        target_pos = self.waypoints[self.current_waypoint_index]
        distance_to_target = np.linalg.norm(target_pos - self.pos)

        if distance_to_target < self.waypoint_threshold:
            self.current_waypoint_index += 1
            if self.current_waypoint_index >= len(self.waypoints):
                self.mission_complete = True
                self.pos = target_pos # Snap to final waypoint
                self.velocity = np.array([0.0, 0.0])
                print(f"Drone {self.id}: Mission Complete!")
                return
            else:
                print(f"Drone {self.id}: Waypoint reached. Moving to next.")
                self._update_target()

        # Move the drone based on its velocity
        # Ensure we don't overshoot the target in one time step
        movement = self.velocity * dt
        if np.linalg.norm(movement) > distance_to_target:
            self.pos = target_pos
        else:
            self.pos += movement

    def is_mission_complete(self) -> bool:
        """Returns True if the drone has visited all its waypoints."""
        return self.mission_complete

    def __repr__(self) -> str:
        """Provides a string representation of the Drone object."""
        return (f"Drone(id={self.id}, pos=[{self.pos[0]:.2f}, {self.pos[1]:.2f}], "
                f"target_wp={self.current_waypoint_index})")
