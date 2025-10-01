# skymind_sim/main.py

import numpy as np
from skymind_sim.core.drone import Drone
from skymind_sim.core.environment import Environment
from skymind_sim.core.simulation import Simulation

def main():
    """
    Main function to set up and run the multi-drone simulation.
    """
    print("Setting up multi-drone simulation...")

    # 1. Create the shared environment
    env = Environment(width=500, height=500)

    # 2. Define waypoints for each drone
    waypoints_alpha = np.array([
        [50, 50],
        [150, 50],
        [150, 150],
        [50, 150],
        [50, 50]  # Return to start
    ], dtype=float)

    waypoints_beta = np.array([
        [450, 450],
        [350, 450],
        [350, 350],
        [450, 350],
        [450, 450] # Return to start
    ], dtype=float)

    # 3. Create drone instances
    drone_alpha = Drone(
        drone_id="drone_alpha",
        start_pos=waypoints_alpha[0],
        waypoints=waypoints_alpha,
        speed=15.0, # m/s
        battery_level=100.0,
        battery_depletion_rate=0.5 # units per second
    )

    drone_beta = Drone(
        drone_id="drone_beta",
        start_pos=waypoints_beta[0],
        waypoints=waypoints_beta,
        speed=20.0, # Let's make this one a bit faster
        battery_level=100.0,
        battery_depletion_rate=0.6 # Faster speed, higher consumption
    )
    
    # 4. Create a list of drones
    all_drones = [drone_alpha, drone_beta]

    # 5. Initialize and run the simulation
    # The time_step can be adjusted for precision vs. performance
    sim = Simulation(drones=all_drones, environment=env, time_step=0.1)
    sim.run()


if __name__ == "__main__":
    main()
