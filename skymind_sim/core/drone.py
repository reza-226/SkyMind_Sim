# skymind_sim/core/drone.py

import numpy as np
from .battery import Battery

class Drone:
    def __init__(self, drone_id: str, start_pos, waypoints, speed: float = 10.0, battery_level: float = 100.0, battery_depletion_rate: float = 0.5):
        self.drone_id = drone_id
        
        # Ensure position and waypoints are float arrays for accurate calculations
        self.pos = np.array(start_pos, dtype=float) 
        self.waypoints = np.array(waypoints, dtype=float)
        
        self.speed = speed  # in meters/second
        self.battery = Battery(initial_level=battery_level)
        self.battery_depletion_rate = battery_depletion_rate # units per second
        
        self.status = "flying"  # Can be 'flying', 'landing', 'landed'
        self.waypoint_index = 0
        self.target_waypoint = self.waypoints[self.waypoint_index]
        
        print(f"Drone {self.drone_id}: Initialized at position {self.pos} with {self.battery.level:.2f}% battery.")
        if self.waypoints.size > 0:
            self.waypoint_index = 1 # Start by heading to the first waypoint in the list
            self.target_waypoint = self.waypoints[self.waypoint_index]
            print(f"Drone {self.drone_id}: Heading to waypoint {self.waypoint_index} at {self.target_waypoint}")


    def update_state(self, time_delta: float):
        """Updates the drone's position and battery based on the time delta."""
        if self.status != "flying":
            return

        # Calculate battery depletion before moving
        self.battery.deplete(self.battery_depletion_rate * time_delta)
        if self.battery.is_empty():
            print(f"Drone {self.drone_id}: Battery depleted! Emergency landing...")
            self.status = "landed" # Or a new 'crashed' status
            return

        # Movement calculation
        direction_vector = self.target_waypoint - self.pos
        distance_to_target = np.linalg.norm(direction_vector)

        travel_distance = self.speed * time_delta

        if travel_distance >= distance_to_target:
            # Reached the waypoint
            self.pos = self.target_waypoint
            print(f"Drone {self.drone_id}: Reached waypoint {self.waypoint_index} at position {self.pos}")

            # Move to the next waypoint
            self.waypoint_index += 1
            if self.waypoint_index < len(self.waypoints):
                self.target_waypoint = self.waypoints[self.waypoint_index]
                print(f"Drone {self.drone_id}: Heading to waypoint {self.waypoint_index} at {self.target_waypoint}")
            else:
                # Mission finished
                print(f"Drone {self.drone_id}: Mission completed. Final status: landed.")
                self.status = "landed"
        else:
            # Move towards the waypoint
            movement_vector = (direction_vector / distance_to_target) * travel_distance
            self.pos += movement_vector
