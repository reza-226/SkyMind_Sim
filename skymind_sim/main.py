# skymind_sim/main.py

# Import standard libraries
import time

# Import core simulation components
from .core.environment import Environment
from .core.drone import Drone
from .core.simulation import Simulation

# Import path planning and visualization
from .pathfinding.path_planner import PathPlanner
from .visualization.visualizer import Visualizer3D

def main():
    """Main function to run the SkyMind simulation."""
    print("--- Initializing SkyMind Simulation ---")
    
    # Define the path to the map file for clarity
    map_filepath = "data/maps/simple_map.json"
    env = Environment(map_file=map_filepath)
    
    # Define start and end points for the drone's mission
    start_point = (10, 10, 5)
    end_point = (80, 80, 15)
    
    # Initialize the path planner with the environment
    planner = PathPlanner(env)
    
    # Plan the path
    print(f"Planning path from {start_point} to {end_point}...")
    path = planner.plan_path(start_point, end_point)
    
    if path:
        print("Path found successfully!")
        
        # ----------------- 3D Visualization -----------------
        print("Generating 3D visualization...")
        visualizer = Visualizer3D(env, start_point, end_point)
        visualizer.draw_obstacles()
        visualizer.draw_path(path)
        visualizer.show() # This will block until the plot window is closed
        
        # ----------- Text-based Simulation (after visualization) -----------
        print("\n--- Starting Text-Based Simulation ---")
        drone = Drone(initial_position=start_point)
        sim = Simulation(env, drone, path)
        sim.run()
    else:
        print("Could not find a path.")
        
    print("--- Simulation Finished ---")

if __name__ == "__main__":
    main()
