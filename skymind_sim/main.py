import numpy as np
from skymind_sim.core.environment import Environment
from skymind_sim.core.path_planner import PathPlanner
# from skymind_sim.core.simulation import Simulation

def main():
    print("Starting SkyMind Simulation...")
    map_path = 'data/maps/basic_map.json'

    try:
        # 1. Initialize Environment
        print(f"Loading map from '{map_path}'...")
        env = Environment(map_path)

        # Get start and end points from the map data
        # Assuming we use the first start/end point defined in the map
        start_position_list = env.map_data['start_points'][0]['position']
        start_point = tuple(start_position_list)

        # Get the 'position' list from the first dictionary in 'end_points'
        end_position_list = env.map_data['end_points'][0]['position']
        end_point = tuple(end_position_list)

        # 2. Initialize Path Planner
        planner = PathPlanner(env)

        # 3. Find Path
        print("Starting path planning...")
        # --- خط زیر را تغییر دهید ---
        path = planner.find_path_a_star(start_point, end_point)

        # 4. Run Simulation
        if path:
            print(f"Path found with {len(path)} points. Starting simulation...")
            # sim = Simulation(env, path)
            # sim.run()
            print("--- Simulation run is commented out for now. ---")
            print("Path starts at:", path[0])
            print("Path ends at:", path[-1])
            # Optional: print a few points from the path
            if len(path) > 10:
                print("Path sample:", path[:5], "...", path[-5:])

        else:
            print("Could not find a path. Simulation will not run.")

    except Exception as e:
        # A more specific error message based on the context
        if 'Environment' in str(e.__class__):
            print(f"An unexpected error occurred during environment setup: {e}")
        elif 'PathPlanner' in str(e.__class__):
             print(f"An unexpected error occurred during path planning: {e}")
        else:
            print(f"An unexpected error occurred: {e}")
            # For debugging, you might want to see the full traceback
            # import traceback
            # traceback.print_exc()

    finally:
        print("Main execution finished.")

if __name__ == "__main__":
    main()
