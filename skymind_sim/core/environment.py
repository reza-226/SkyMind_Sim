# FILE: skymind_sim/core/environment.py

import random
from skymind_sim.core.drone import Drone

class Environment:
    """
    Manages all objects within the simulation space,
    including drones and potential obstacles.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.drones = []
        self.obstacles = []
        self._drone_id_counter = 0

    def add_drone(self, drone):
        """Adds a single drone to the environment."""
        self.drones.append(drone)

    def create_drones(self, count):
        """
        Creates a specified number of drones with random initial positions
        and adds them to the environment.
        """
        for _ in range(count):
            # Create a unique name for each drone
            drone_name = f"Drone-{self._drone_id_counter}"
            self._drone_id_counter += 1
            
            # Generate random positions within the screen boundaries (with a margin)
            rand_x = random.randint(50, self.width - 50)
            rand_y = random.randint(50, self.height - 50)
            
            # Create a new drone instance
            new_drone = Drone(drone_id=self._drone_id_counter, name=drone_name, position=[rand_x, rand_y])
            
            # Add the new drone to our list
            self.add_drone(new_drone)
        
        print(f"Created and added {count} drones to the environment.")

    def get_all_drones(self):
        """Returns the list of all drones."""
        return self.drones

    def update_all(self):
        """Updates the state of all objects in the environment."""
        for drone in self.drones:
            drone.update_state(self.width, self.height)
