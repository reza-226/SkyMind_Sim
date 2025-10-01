# skymind_sim/main.py

import numpy as np
from skymind_sim.core import Simulation, Environment, Drone

def main():
    """
    Main function to set up and run the simulation.
    """
    print("Setting up multi-drone simulation...")

    # 1. Create the Environment
    # The environment now only needs its size.
    env = Environment(size=(800, 600))

    # 2. Define Drone Configurations
    # This dictionary-based approach is clean and scalable.
    drones_config = {
        "drone_1": {
            "pos": np.array([50.0, 50.0]),
            "waypoints": [
                np.array([100.0, 100.0]),
                np.array([200.0, 400.0]),
                np.array([50.0, 500.0]),
            ]
        },
        "drone_2": {
            "pos": np.array([750.0, 550.0]),
            "waypoints": [
                np.array([600.0, 500.0]),
                np.array([400.0, 200.0]),
                np.array([700.0, 100.0]),
            ]
        },
        "drone_3": {
            "pos": np.array([400.0, 300.0]),
            "waypoints": [
                np.array([100.0, 300.0]),
                np.array([400.0, 500.0]),
                np.array([700.0, 300.0]),
                np.array([400.0, 100.0]),
            ]
        }
    }

    # 3. Create Drone instances from the configuration
    drones: dict[str, Drone] = {}
    for drone_id, config in drones_config.items():
        drones[drone_id] = Drone(
            id=drone_id,
            pos=config["pos"],
            waypoints=config["waypoints"]
        )
        print(f"- Created {drone_id} at start position {config['pos']}")


    # 4. Create the Simulation instance
    # Pass the already created environment and drones dictionary.
    sim = Simulation(env=env, drones=drones, viz_enabled=True)

    # 5. Run the simulation for a total of 100 seconds
    sim.run(until=100.0)

    print("Simulation setup complete. Running...")


if __name__ == "__main__":
    main()
