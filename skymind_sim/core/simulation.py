# skymind_sim/core/simulation.py

import numpy as np
from .environment import Environment
from .drone import DroneStatus # Import DroneStatus for type checking

class Simulation:
    """
    Manages the state and progression of the drone simulation.
    """
    def __init__(self, environment: Environment):
        if not isinstance(environment, Environment):
            raise TypeError("The provided environment is not a valid Environment object.")
        
        self.environment = environment
        self.history = []
        self._is_running = False
        self.time = 0.0

    def _update_drone_state(self, drone, dt: float):
        """
        Updates a single drone's state based on time delta (dt).
        This is a simplified physics model.
        """
        # A simple movement model: position = position + velocity * dt
        if drone.status == DroneStatus.FLYING:
            new_position = drone.position + drone.velocity * dt
            drone.move_to(new_position)

    def _record_state(self, step: int, time: float):
        """
        Private method to record the state of all drones at a specific step.
        """
        drones_state = []
        for drone in self.environment.get_drones():
            drones_state.append({
                'id': drone.id,  # Correctly uses drone.id
                'position': drone.position.tolist(), # Convert numpy array to list for serialization
                'velocity': drone.velocity.tolist(),
                'status': drone.status.value # Use .value to get the string from Enum
            })

        self.history.append({
            'step': step,
            'time': time,
            'drones': drones_state
        })

    def run(self, num_steps: int, dt: float = 0.1):
        """
        Runs the simulation for a given number of steps.
        
        Args:
            num_steps (int): The number of simulation steps to execute.
            dt (float): The time delta for each step in seconds.
        """
        if self._is_running:
            print("Simulation is already running.")
            return

        print(f"Starting simulation for {num_steps} steps with dt={dt}s...")
        self._is_running = True
        
        # Record initial state (step 0)
        if not self.history:
            self._record_state(step=0, time=self.time)

        for i in range(1, num_steps + 1):
            current_step = len(self.history)
            self.time += dt
            
            # Update each drone in the environment
            for drone in self.environment.get_drones():
                self._update_drone_state(drone, dt)
                
            # Record the state after updates
            self._record_state(step=current_step, time=self.time)

        self._is_running = False
        print("Simulation finished.")

    def reset(self):
        """Resets the simulation to its initial state."""
        self.history = []
        self.time = 0.0
        self._is_running = False
        # Note: This does not reset the state of drones in the environment.
        # A more complex implementation might be needed for that.
        print("Simulation has been reset.")
