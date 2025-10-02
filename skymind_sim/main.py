# skymind_sim/main.py

import pygame
import logging
from .layer_0_presentation.renderer import Renderer
from .layer_1_simulation.simulation import Simulation
from .utils.logger import setup_logging

# --- Configuration ---
WINDOW_TITLE = "SkyMind_Sim"
MAP_FILE_PATH = "data/maps/simple_map.json"  # Path to our new map file
LOG_LEVEL = logging.INFO

def main():
    # 1. Initialization
    setup_logging(LOG_LEVEL)
    logger = logging.getLogger(__name__)
    pygame.init()
    
    # 2. Layer Setup
    # Layer 1: Simulation Core
    simulation = Simulation()
    simulation.load_world_from_file(MAP_FILE_PATH)
    
    # Get world size from the simulation after loading the map
    world_size = simulation.get_world_state()["world_size"]

    # Layer 0: Presentation
    renderer = Renderer(width=world_size[0], height=world_size[1], title=WINDOW_TITLE)
    renderer.load_assets()

    # --- Temp: Set a simple path for the drone to test movement ---
    # In the future, this path will come from Layer 3 (Intelligence)
    simulation.set_drone_path("d1", [(700, 500), (700, 100), (100, 100), (100, 500)])


    # 3. Main Loop
    running = True
    clock = pygame.time.Clock()
    logger.info("Starting Main Loop...")
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 4. Logic & Update
        simulation.update(dt)

        # 5. Rendering
        world_state = simulation.get_world_state()
        renderer.render(world_state)

    logger.info("...Main Loop Exited.")

    # 6. Cleanup
    renderer.cleanup()
    pygame.quit()
    logger.info("Application Closed")

if __name__ == "__main__":
    main()
