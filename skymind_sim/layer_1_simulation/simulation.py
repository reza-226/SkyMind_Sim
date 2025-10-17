# skymind_sim/layer_1_simulation/simulation.py

import pygame
import logging
from skymind_sim.layer_1_simulation.world.world import World
from skymind_sim.layer_0_presentation.renderer import Renderer
from skymind_sim.layer_0_presentation.camera import Camera
from skymind_sim.layer_0_presentation.input_handler import InputHandler
from skymind_sim.utils.config_loader import ConfigLoader

class Simulation:
    """Main class to run the simulation and manage the game loop."""

    def __init__(self, config_path=None):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing Simulation components...")
        
        # Load configurations
        sim_config = ConfigLoader.get('simulation')
        self.fps = sim_config.get('fps', 60)
        self.should_run = True

        # --- REORDERED INITIALIZATION ---

        # 1. Initialize Renderer first to set up the Pygame display mode
        self.renderer = Renderer()
        
        # 2. Initialize World and its entities (now that display mode is set)
        self.world = World()
        self.player_drone = self.world.get_player_drone()
        
        # 3. Initialize Camera with all required dimensions
        screen_size = self.renderer.get_screen_size()
        world_pixel_size = self.world.grid.get_world_size_in_pixels()
        self.camera = Camera(
            target=self.player_drone,
            screen_width=screen_size[0],
            screen_height=screen_size[1],
            world_width=world_pixel_size[0],
            world_height=world_pixel_size[1]
        )
        
        # Update renderer with the camera it needs to use
        self.renderer.set_camera(self.camera)

        # 4. Initialize other components
        self.input_handler = InputHandler()

        # ------------------------------------
        
        self.clock = pygame.time.Clock()
        self.logger.info("Simulation initialized successfully.")

    def run(self):
        """Starts the main simulation loop."""
        self.logger.info("Simulation loop started.")
        
        while self.should_run:
            dt = self.clock.tick(self.fps) / 1000.0
            self._handle_events()
            self._update(dt)
            self._render()

        self.logger.info("Simulation loop finished.")

    def _handle_events(self):
        """Processes user input and other events."""
        events_result = self.input_handler.handle_events()
        
        if events_result["quit"]:
            self.should_run = False
        
        self.movement_intent = events_result["movement_intent"]

    def _update(self, dt: float):
        """Updates the state of all simulation objects."""
        if self.player_drone:
            self.player_drone.move(self.movement_intent)
        
        self.world.update(dt)
        self.camera.update(dt)

    def _render(self):
        """Renders the simulation state to the screen."""
        self.renderer.render(self.world)

    def stop(self):
        """Stops the simulation."""
        self.should_run = False
