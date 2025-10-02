# skymind_sim/core/simulation.py
import pygame
import sys

from .drone import Drone

class Simulation:
    def __init__(self, config, environment):
        """
        Initializes the main simulation logic.
        
        :param config: The simulation configuration dictionary.
        :param environment: The initialized Environment object.
        """
        print("INFO: Initializing Simulation...")
        self.config = config
        self.environment = environment # The environment now handles the window and clock

        # --- Create Game Objects ---
        # Create a sprite group to hold all sprites for easy updating and drawing
        self.all_sprites = pygame.sprite.Group()

        # Create the drone and add it to the sprite group
        start_x = self.config.get('SCREEN_WIDTH', 1280) / 2
        start_y = self.config.get('SCREEN_HEIGHT', 720) / 2
        self.drone = Drone(start_pos=(start_x, start_y))
        self.all_sprites.add(self.drone)

        print("INFO: Simulation created.")

    def run(self):
        """
        The main loop of the simulation.
        """
        print("INFO: Simulation is running...")
        while self.environment.running:
            # --- Event Handling ---
            # Get all events from the queue
            events = pygame.event.get()
            self.environment.handle_events(events)

            # --- Update Phase ---
            # Update all sprites in the group
            self.all_sprites.update()
            self.environment.update()

            # --- Render Phase ---
            # The environment handles drawing the background and sprites
            self.environment.render(self.all_sprites)

            # --- Frame Rate Control ---
            # Ensure the loop runs at a maximum of FPS frames per second
            self.environment.clock.tick(self.config.get('FPS', 60))

        # --- Quit ---
        print("INFO: Simulation loop ended. Quitting...")
        pygame.quit()
        sys.exit()
