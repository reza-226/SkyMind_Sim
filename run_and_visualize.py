# path: run_and_visualize.py

import sys
import pygame
from skymind_sim.utils.log_manager import LogManager
from skymind_sim.utils.config_manager import ConfigManager
from skymind_sim.layer_1_simulation.simulation import Simulation
from skymind_sim.layer_0_presentation.renderer import Renderer

def main():
    """
    Main function to initialize and run the simulation and visualization.
    """
    # 1. Initialize the Logger (must be first)
    # No need for a variable, LogManager is a static class now
    LogManager.init()
    main_logger = LogManager.get_logger(__name__)
    main_logger.info("Application starting...")

    try:
        # 2. Initialize the Configuration Manager
        config_manager = ConfigManager('data/config')
        if not config_manager.get_all_configs():
            main_logger.error("Configuration is empty. Check the config path and files.")
            return

        # 3. Initialize the main Simulation object
        # The Simulation will create its own components like World and Scheduler
        simulation = Simulation(config_manager)

        # 4. Add agents (e.g., drones) to the simulation
        # The start_pos_key tells the simulation where to look for the drone's start position.
        # This key MUST match the structure of your JSON files.
        simulation.add_agent(drone_id="drone_0", start_pos_key='drone.drone_0.start_position')

        # 5. Initialize the Renderer
        renderer = Renderer(config_manager, simulation.world)

        # 6. Main simulation loop
        main_logger.info("Entering main simulation loop...")
        running = True
        clock = pygame.time.Clock()
        
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            # Simulation logic step
            simulation.step()

            # Rendering step
            renderer.render_all(simulation.agents)

            # Control the frame rate
            clock.tick(config_manager.get('simulation.run_control.fps', 30))

    except Exception as e:
        main_logger.critical(f"A critical error occurred: {e}", exc_info=True)
        # exc_info=True will log the full traceback
    finally:
        main_logger.info("Application shutting down.")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
