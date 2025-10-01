# FILE: skymind_sim/main.py

import pygame
import numpy as np
import sys
import os

# Adjust the Python path to include the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skymind_sim.core.drone import Drone
from skymind_sim.core.environment import Environment
from skymind_sim.core.simulation import Simulation

# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

def main():
    """
    Main function to initialize and run the simulation.
    """
    # --- Pygame Setup ---
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SkyMind Drone Simulation")

    print("Simulation setup starting...")

    # --- Environment Setup ---
    env = Environment(width=WIDTH, height=HEIGHT)

    # --- Create Drone Instances with Correct Parameter Name ---
    # --- MODIFIED LINES ---
    drone1 = Drone(drone_id="UAV_1", position=np.array([50.0, 50.0]))
    drone2 = Drone(drone_id="UAV_2", position=np.array([750.0, 550.0]))
    drone3 = Drone(drone_id="UAV_3", position=np.array([400.0, 300.0]))
    # --- END OF MODIFIED LINES ---

    # --- Define Missions for Drones ---
    # Mission for UAV_1: Patrol a triangular area
    path1 = [np.array([200.0, 200.0]), np.array([50.0, 400.0]), np.array([300.0, 50.0])]
    drone1.set_mission(path1)

    # Mission for UAV_2: Move to a single point and stay
    path2 = [np.array([100.0, 100.0])]
    drone2.set_mission(path2)

    # Mission for UAV_3: Go to a point near the center
    path3 = [np.array([300.0, 350.0])]
    drone3.set_mission(path3)

    # --- Add Drones to Environment ---
    env.add_drone(drone1)
    env.add_drone(drone2)
    env.add_drone(drone3)

    # --- Simulation Setup ---
    sim = Simulation(environment=env, screen=screen, width=WIDTH, height=HEIGHT)

    # --- Run Simulation ---
    sim.run()

    # --- Shutdown ---
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
