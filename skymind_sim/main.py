# skymind_sim/main.py

import logging
import uuid
from skymind_sim.core.drone import Drone
from skymind_sim.core.environment import Environment
from skymind_sim.core.simulation import Simulation

# --- Basic Logger Configuration ---
# Create a logger
logger = logging.getLogger("simulation_log")
logger.setLevel(logging.INFO) # Set the lowest level of messages to handle

# Create handlers
# Console handler for printing logs to the screen
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO) # Only INFO and above will be shown in console

# File handler for saving logs to a file
f_handler = logging.FileHandler('data/simulation_logs/sim_run.log', mode='w')
f_handler.setLevel(logging.DEBUG) # DEBUG and above will be saved to the file

# Create formatters and add it to handlers
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(log_format)
f_handler.setFormatter(log_format)

# Add handlers to the logger
if not logger.handlers:
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

# --- Main Simulation Setup ---
def main():
    """
    Sets up and runs a multi-drone simulation scenario.
    """
    logger.info("Setting up the simulation scenario.")

    try:
        # 1. Initialize the Environment with a map
        # The environment is now the central manager of the grid and drones.
        map_path = 'data/maps/map1.txt'
        environment = Environment(map_file=map_path)

        # 2. Create and Add Drones to the Environment
        # We create multiple drone instances and add them one by one.
        # The environment will handle path calculation for each.
        
        # Drone Alpha
        drone_alpha = Drone(
            drone_id=f"alpha-{str(uuid.uuid4())[:4]}",
            start_pos=(1, 1),
            char='A'
        )
        environment.add_drone(drone_alpha, end_pos=(5, 17)) # Corrected end position

        # Drone Bravo
        drone_bravo = Drone(
            drone_id=f"bravo-{str(uuid.uuid4())[:4]}",
            start_pos=(8, 1),
            char='B'
        )
        environment.add_drone(drone_bravo, end_pos=(1, 15))

        # Drone Charlie
        drone_charlie = Drone(
            drone_id=f"charlie-{str(uuid.uuid4())[:4]}",
            start_pos=(3, 3),
            char='C'
        )
        environment.add_drone(drone_charlie, end_pos=(8, 12))

        # 3. Initialize the Simulation Engine
        # The simulation engine now takes the whole environment.
        simulation = Simulation(environment, time_step=0.3)

        # 4. Run the simulation
        simulation.run()

    except (FileNotFoundError, ValueError) as e:
        logger.error(f"Failed to initialize simulation: {e}")
        print(f"Error: Could not set up the simulation. Please check logs for details.")
    except Exception as e:
        logger.critical(f"An unexpected critical error occurred: {e}", exc_info=True)
        print("A critical error occurred. The simulation has been aborted.")

if __name__ == "__main__":
    main()
