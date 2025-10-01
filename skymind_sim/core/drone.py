# FILE: skymind_sim/core/drone.py

import numpy as np
from enum import Enum

class DroneStatus(Enum):
    IDLE = "Idle"
    MOVING = "Moving"
    CHARGING = "Charging"
    RETURNING = "Returning"

class Drone:
    """
    Represents a single drone in the simulation.
    """
    def __init__(self, drone_id, position, battery=100, speed=1):
        """
        Initializes a Drone object.

        Args:
            drone_id (str): The unique identifier for the drone.
            position (np.ndarray): The initial (x, y) coordinates of the drone.
            battery (int): The initial battery level (0-100).
            speed (float): The speed of the drone in units per simulation step.
        """
        self.drone_id = drone_id
        self.position = np.array(position, dtype=float)
        self.battery = battery
        self.speed = speed
        self.status = DroneStatus.IDLE
        self.mission_path = []

    def set_mission(self, waypoints):
        """
        Sets a mission for the drone, defined by a list of waypoints.

        Args:
            waypoints (list of tuples/np.ndarray): A list of (x, y) coordinates.
        """
        self.mission_path = [np.array(wp, dtype=float) for wp in waypoints]
        if self.mission_path:
            self.status = DroneStatus.MOVING
            print(f"Drone {self.drone_id}: Mission set. Path: {self.mission_path}")

    def update(self, delta_time):
        """
        Updates the drone's state for a single time step.
        This includes moving towards a waypoint and consuming battery.
        """
        if self.status == DroneStatus.MOVING and self.mission_path:
            target = self.mission_path[0]
            direction = target - self.position
            distance = np.linalg.norm(direction)
            
            travel_distance = self.speed * delta_time
            
            if distance <= travel_distance:
                # Reached the waypoint
                self.position = target
                self.mission_path.pop(0)
                if not self.mission_path:
                    self.status = DroneStatus.IDLE
                    print(f"Drone {self.drone_id} completed its mission.")
            else:
                # Move towards the waypoint
                self.position += (direction / distance) * travel_distance
            
            # Consume battery (simple model)
            self.battery -= 0.1 * delta_time 
            if self.battery < 0:
                self.battery = 0

    def __str__(self):
        return (f"Drone(ID={self.drone_id}, Pos={self.position}, "
                f"Battery={self.battery:.1f}%, Status={self.status.value})")
