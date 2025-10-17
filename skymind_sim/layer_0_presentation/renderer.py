# skymind_sim/layer_0_presentation/renderer.py
import pygame
import logging
from typing import Optional

from skymind_sim.utils.config_loader import ConfigLoader
# We need Camera for type hinting, but to avoid circular import, use a string
# from skymind_sim.layer_0_presentation.camera import Camera

class Renderer:
    """Handles all drawing operations for the simulation."""

    def __init__(self):
        """Initializes Pygame, the display window, and the font."""
        self.logger = logging.getLogger(__name__)

        window_config = ConfigLoader.get('window')
        self.width = window_config.get('width', 1280)
        self.height = window_config.get('height', 720)
        self.caption = window_config.get('caption', 'SkyMind Drone Simulation')
        self.bg_color = tuple(window_config.get('bg_color', [0, 0, 0]))

        # Initialize Pygame and the display window
        pygame.init()
        pygame.display.set_caption(self.caption)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.logger.info(f"Display initialized with size {self.width}x{self.height}.")
        
        self.camera: Optional['Camera'] = None

    def set_camera(self, camera: 'Camera'):
        """Sets the camera object for the renderer."""
        self.camera = camera
        self.logger.info("Camera has been set for the renderer.")

    def render(self, world):
        """
        Renders the entire simulation world for one frame.

        Args:
            world: The World object containing all game elements.
        """
        if not self.camera:
            self.logger.error("Renderer cannot render without a camera.")
            return

        # 1. Fill the background
        self.screen.fill(self.bg_color)

        # 2. Get the camera offset
        camera_offset = self.camera.get_offset()

        # 3. Draw the world (which will draw the grid and entities)
        world.draw(self.screen, camera_offset)

        # 4. Update the display
        pygame.display.flip()
        
    def get_screen_size(self) -> tuple[int, int]:
        """Returns the screen size (width, height)."""
        return self.width, self.height
