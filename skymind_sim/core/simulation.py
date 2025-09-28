# skymind_sim/core/simulation.py

import numpy as np
from collections import defaultdict
from .environment import Environment

class Simulation:
    """
    Manages the execution of the simulation over time, updating the state of all drones.
    """

    def __init__(self, env: Environment):
        """
        Initializes the simulation.

        Args:
            env (Environment): The simulation environment containing the drones.
        """
        self.environment = env
        self.history = defaultdict(list)
        self.time = 0.0

    def run(self, num_steps: int, dt: float):
        """
        Runs the simulation for a given number of steps.

        Args:
            num_steps (int): The number of steps to simulate.
            dt (float): The time delta for each step in seconds.
        """
        print(f"Starting simulation for {num_steps} steps with dt={dt}...")
        
        # Record initial positions
        print(f"Recording initial positions at t={self.time:.1f}s...")
        for drone in self.environment.drones:
            # FIX: Append a tuple of (time, x, y, z)
            # The * operator unpacks the drone.position array [x, y, z] into x, y, z
            self.history[drone.drone_id].append((self.time, *drone.position))

        for step in range(1, num_steps + 1):
            self.time += dt
            
            for drone in self.environment.drones:
                drone.update_state(dt)
                
                # FIX: Append a tuple of (time, x, y, z) for the new position
                self.history[drone.drone_id].append((self.time, *drone.position))

            if step % 50 == 0 or step == num_steps:
                print(f"  ... Step {step}/{num_steps} completed. Current time: {self.time:.2f}s")
        
        print("Simulation finished.")
        return self.history
