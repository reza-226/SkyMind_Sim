# skymind_sim/core/drone.py

import numpy as np

class Drone:
    """
    Represents a single drone in the simulation.
    Manages its own state, including position, status, and battery.
    """
    def __init__(self, drone_id: str, start_pos: np.ndarray, speed: float = 10.0, waypoints: list = None, battery_level: float = 100.0):
        """
        Initializes a Drone instance.

        Args:
            drone_id (str): A unique identifier for the drone.
            start_pos (np.ndarray): The starting position (x, y) of the drone.
            speed (float): The travel speed of the drone in units per second.
            waypoints (list, optional): A list of waypoints for the drone's mission. Defaults to None.
            battery_level (float, optional): The initial battery level percentage. Defaults to 100.0.
        """
        self.drone_id = drone_id
        
        # CRITICAL FIX: Initialize self.pos as a float array to allow for fractional positions.
        self.pos = np.array(start_pos, dtype=float) 
        
        self.speed = speed
        
        # Ensure waypoints are also float arrays for consistency
        self.waypoints = [np.array(wp, dtype=float) for wp in waypoints] if waypoints else []
        
        self.current_waypoint_index = 0
        self.status = "idle"

        # Battery properties
        self.battery_level = battery_level
        self.consumption_rate_flying = 0.5
        self.consumption_rate_hovering = 0.1
    
    def start_mission(self):
        """Starts the mission by setting status to flying if waypoints are available."""
        if self.waypoints:
            print(f"Drone {self.drone_id}: Mission started. Heading to waypoint {self.current_waypoint_index}.")
            self.status = "flying"
        else:
            print(f"Drone {self.drone_id}: No waypoints defined. Mission cannot start.")
            self.status = "idle"

    def update_state(self, time_delta: float):
        """
        Updates the drone's state for a given time delta.
        This includes position and battery, and handles state transitions like
        reaching a waypoint or crashing.
        """
        if self.status not in ["flying", "hovering"]:
            return

        # 1. Update Battery
        consumption = 0
        if self.status == "flying":
            consumption = self.consumption_rate_flying * time_delta
        elif self.status == "hovering":
            consumption = self.consumption_rate_hovering * time_delta
        
        self.battery_level -= consumption
        
        if self.battery_level <= 0:
            self.battery_level = 0
            self.status = "crashed"
            print(f"\nCRITICAL: Drone {self.drone_id} ran out of battery and crashed at position {self.pos}!")
            return

        # 2. Update Position if flying
        if self.status == "flying":
            if self.current_waypoint_index >= len(self.waypoints):
                self.status = "landed"
                return

            target_pos = self.waypoints[self.current_waypoint_index]
            direction = target_pos - self.pos
            distance_to_target = np.linalg.norm(direction)

            if distance_to_target == 0:
                self._waypoint_reached()
                return

            travel_distance = self.speed * time_delta
            
            if travel_distance >= distance_to_target:
                self.pos = target_pos
                self._waypoint_reached()
            else:
                # This line requires self.pos to be a float array.
                self.pos += (direction / distance_to_target) * travel_distance

    def _waypoint_reached(self):
        """Internal helper method to handle logic when a waypoint is reached."""
        print(f"Drone {self.drone_id}: Reached waypoint {self.current_waypoint_index} at position {self.pos}")
        self.current_waypoint_index += 1
        
        if self.current_waypoint_index >= len(self.waypoints):
            self.status = "landed"
            print(f"Drone {self.drone_id}: Mission completed. Final status: landed.")
