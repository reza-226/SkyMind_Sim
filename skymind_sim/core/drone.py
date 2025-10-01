# skymind_sim/core/drone.py

import numpy as np

class Drone:
    """
    Represents a single drone in the simulation, managing its state,
    mission, and physical properties like battery.
    """
    def __init__(self, drone_id, position, speed,
                 battery_capacity=1000.0, consumption_rate=1.0):
        """
        Initializes a Drone object.

        Args:
            drone_id (str): Unique identifier for the drone.
            position (list or np.ndarray): Initial position [x, y].
            speed (float): The speed of the drone in units per second.
            battery_capacity (float): Maximum battery capacity (e.g., in abstract energy units).
            consumption_rate (float): Energy consumed per second of flight.
        """
        self.id = drone_id
        self.position = np.array(position, dtype=float)
        self.speed = speed
        self.path = []
        self.path_index = 0
        self.is_mission_complete = False

        # --- Battery Attributes ---
        self.battery_capacity = float(battery_capacity)
        self.current_battery = float(battery_capacity)  # Start with a full battery
        self.consumption_rate = float(consumption_rate)
        self.is_active = True  # A flag to indicate if the drone can fly

    def __repr__(self):
        """Provides a developer-friendly representation of the drone."""
        return (f"Drone(id={self.id}, pos={self.position}, "
                f"battery={self.current_battery:.2f}/{self.battery_capacity:.2f}, "
                f"active={self.is_active})")

    def set_mission(self, path):
        """
        Assigns a mission (a series of waypoints) to the drone.

        Args:
            path (list of lists): A list of [x, y] coordinates representing the path.
        """
        self.path = [np.array(p, dtype=float) for p in path]
        self.path_index = 0
        self.is_mission_complete = False
        print(f"Drone {self.id}: Mission set. Path: {self.path}")

    def update(self, dt):
        """
        Updates the drone's state for a given time step (dt).
        This includes movement and battery consumption.

        Args:
            dt (float): The time elapsed since the last update in seconds.
        """
        # --- Pre-update Checks ---
        # Do nothing if mission is done or drone is out of battery
        if self.is_mission_complete or not self.is_active:
            return

        # Check if we are at the end of the path list
        if self.path_index >= len(self.path):
            self.is_mission_complete = True
            print(f"Drone {self.id}: Mission Complete!")
            return

        # --- Energy Consumption ---
        energy_consumed = self.consumption_rate * dt
        
        # Check if there's enough battery for this time step
        if self.current_battery <= energy_consumed:
            self.current_battery = 0
            self.is_active = False
            print(f"!!! CRITICAL: Drone {self.id} out of battery at position {self.position} !!!")
            return  # Stop all actions

        # If there's battery, consume it for this time step
        self.current_battery -= energy_consumed

        # --- Movement Logic ---
        target_pos = self.path[self.path_index]
        direction = target_pos - self.position
        distance_to_target = np.linalg.norm(direction)
        
        move_distance = self.speed * dt

        if distance_to_target < move_distance:
            # We are close enough to snap to the target waypoint
            self.position = target_pos
            self.path_index += 1
            # Check if this was the last point in the mission
            if self.path_index >= len(self.path):
                self.is_mission_complete = True
                print(f"Drone {self.id}: Mission Complete!")
        else:
            # Move towards the target
            self.position += (direction / distance_to_target) * move_distance
