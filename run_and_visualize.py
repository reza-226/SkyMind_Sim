# run_and_visualize.py

import pygame
import sys

from skymind_sim.utils.log_manager import LogManager
from skymind_sim.layer_0_presentation.asset_loader import AssetLoader
from skymind_sim.layer_1_simulation.simulation import Simulation
from skymind_sim.layer_0_presentation.renderer import Renderer

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 750
FPS = 30
MAP_FILE_PATH = 'data/maps/simple_map.json'

def main():
    """Main function to run the simulation and visualization."""
    logger = LogManager.get_logger(__name__)
    logger.info("Starting SkyMind Simulator...")

    screen = None # Initialize screen to None
    try:
        # --- START OF MAJOR CHANGES ---
        
        # 1. Initialize Pygame and create the display surface (screen) immediately.
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("SkyMind Simulator")

        # 2. Now that a video mode is set, initialize the AssetLoader.
        asset_loader = AssetLoader(base_path='assets')

        # 3. Initialize Simulation.
        logger.info(f"Initializing simulation with map: '{MAP_FILE_PATH}'")
        simulation = Simulation(map_file_path=MAP_FILE_PATH)
        logger.info(f"Simulation successfully initialized.")

        # Get grid dimensions for the renderer
        grid_dims = simulation.get_grid().get_dimensions()

        # 4. Initialize Renderer and pass the already created screen to it.
        renderer = Renderer(
            screen=screen, # Pass the screen object
            asset_loader=asset_loader,
            grid_dims=grid_dims
        )
        
        # --- END OF MAJOR CHANGES ---

        clock = pygame.time.Clock()
        running = True
        logger.info("Starting simulation loop...")

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            delta_time = clock.tick(FPS) / 1000.0
            simulation.update(delta_time)
            renderer.render_all(simulation)
        
    except Exception as e:
        logger.error(f"An unhandled error occurred: {e}", exc_info=True)
    finally:
        logger.info("Shutting down SkyMind Simulator.")
        pygame.quit() # Simplified shutdown
        sys.exit()

if __name__ == '__main__':
    main()
