# skymind_sim/main.py
import sys
import pygame

from .config import SIM_CONFIG
from .core.simulation import Simulation
from .core.environment import Environment
from .utils.asset_loader import AssetLoader
# Configuration dictionary
SIM_CONFIG = {
    'SCREEN_WIDTH': 1280,
    'SCREEN_HEIGHT': 720,
    'FPS': 60,
    'CAPTION': 'SkyMind Drone Simulator',
    'BACKGROUND_COLOR': (20, 30, 40), # Dark blue-grey
    'ASSETS_DIR': 'assets'
}

def main():
    """The main entry point of the simulator."""
    
    # 1. Initialize core systems IN THE CORRECT ORDER
    
    # First, create the environment, which initializes pygame and the display
    env = Environment(config=SIM_CONFIG)
    
    # Second, load assets now that the display is ready
    AssetLoader.load_assets()
    
    # Third, create the simulation instance
    sim = Simulation(config=SIM_CONFIG, environment=env)

    # 2. Run the main simulation loop
    try:
        sim.run()
    except Exception as e:
        print(f"FATAL: An error occurred during simulation run: {e}")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()