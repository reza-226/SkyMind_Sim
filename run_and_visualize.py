# run_and_visualize.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from skymind_sim.core import Environment, Drone, Simulation

def plot_drone_paths(history, dimensions):
    """
    Plots the 3D paths of all drones from the simulation history.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    for drone_id, path in history.items():
        # Unzip the path data
        times, x_coords, y_coords, z_coords = zip(*path)
        
        # Plot the path
        ax.plot(x_coords, y_coords, z_coords, marker='o', linestyle='-', markersize=2, label=f'Drone {drone_id}')
        
        # Mark start (green) and end (red) points
        ax.scatter(x_coords[0], y_coords[0], z_coords[0], c='green', s=100, label=f'Start D{drone_id}')
        ax.scatter(x_coords[-1], y_coords[-1], z_coords[-1], c='red', s=100, label=f'End D{drone_id}')

    # Set plot limits and labels
    w, h, d = dimensions
    ax.set_xlim(-w / 2, w / 2)
    ax.set_ylim(-h / 2, h / 2)
    ax.set_zlim(0, d)
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')
    ax.set_zlabel('Z coordinate')
    ax.set_title('Drone Simulation Paths')
    ax.legend()
    ax.grid(True)
    
    plt.show()


def main():
    """
    Main function to set up and run the simulation.
    """
    print("--- Setting up the simulation environment ---")
    
    # 1. Create Environment
    dims = (200, 200, 100) # Width, Height, Depth
    print(f"Creating environment with dimensions (W: {dims[0]}, H: {dims[1]}, D: {dims[2]})...")
    env = Environment(width=dims[0], height=dims[1], depth=dims[2])

    # 2. Create and Add Drones
    print("Creating and adding drones to the environment...")
    
    # FIX: Remove the `drone_id` argument as it's now auto-generated.
    pos1 = np.array([50, 50, 10])
    drone1 = Drone(position=pos1)
    print(f"Drone {drone1.drone_id} created at position {drone1.position}")

    pos2 = np.array([-20, 30, 5])
    drone2 = Drone(position=pos2)
    print(f"Drone {drone2.drone_id} created at position {drone2.position}")

    pos3 = np.array([0, -80, 15])
    drone3 = Drone(position=pos3)
    print(f"Drone {drone3.drone_id} created at position {drone3.position}")
    
    env.add_drone(drone1)
    env.add_drone(drone2)
    env.add_drone(drone3)
    print("Drones added successfully.")

    # 3. Assign Missions
    print("Assigning missions to drones...")
    drone1.set_mission(target=np.array([100, 100, 20]), speed=10.0)
    drone2.set_mission(target=np.array([-50, -50, 10]), speed=12.0)
    drone3.set_mission(target=np.array([80, -30, 25]), speed=8.0)
    
    print("--- Environment setup complete ---\n")

    # 4. Create and Run Simulation
    print("--- Running simulation ---")
    sim = Simulation(env)
    history = sim.run(num_steps=300, dt=0.2)
    
    print("\n--- Visualizing results ---")
    plot_drone_paths(history, dims)


if __name__ == "__main__":
    main()
