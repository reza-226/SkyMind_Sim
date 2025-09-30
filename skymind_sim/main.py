# skymind_sim/main.py

import numpy as np

from skymind_sim.core.environment import Environment
from skymind_sim.core.drone import Drone
from skymind_sim.core.simulation import Simulation

def run_basic_mission():
    """
    Sets up and runs a basic mission with one drone and a few waypoints
    using the new event-driven architecture.
    """
    print("Setting up basic mission...")
    
    # 1. Initialize the Environment
    # FIX: Provided the required 'width' and 'height' arguments.
    env = Environment(width=500, height=500)
    print(f"Environment initialized with size {env.width}x{env.height}. No map loaded.")

    # 2. Define Mission Waypoints
    # These coordinates are relative to the environment's origin (0,0)
    # The drone will fly a square pattern.
    waypoints = [
        np.array([200, 50]),
        np.array([200, 200]),
        np.array([50, 200]),
        np.array([50, 50]),
    ]

    # 3. Initialize the Drone
    drone = Drone(
        drone_id="drone_1", 
        start_pos=np.array([50, 50]), 
        speed=10.0,
        waypoints=waypoints
    )

    # 4. Initialize and Run the Simulation
    sim = Simulation(environment=env, drones=[drone])
    
    # The run method now orchestrates the event-driven simulation.
    sim.run()

if __name__ == "__main__":
    run_basic_mission()
