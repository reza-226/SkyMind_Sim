# skymind_sim/layer_1_simulation/entities/drone.py

import pygame
from pygame.math import Vector2
import logging

from skymind_sim.utils.config_loader import ConfigLoader
from skymind_sim.layer_0_presentation.asset_loader import AssetLoader

class Drone:
    """Represents a drone in the simulation."""

    def __init__(self, drone_id: str, grid, position=(0.0, 0.0)):
        self.logger = logging.getLogger(__name__)
        self.id = drone_id
        self.grid = grid
        
        # Position and Movement
        self.position = Vector2(position)  # Grid coordinates (can be float for smooth movement)
        self.velocity = Vector2(0, 0)
        
        # Load drone-specific configuration
        config = ConfigLoader.get('drone')
        self.speed = config.get('speed', 5.0)  # Grid units per second
        self.image_name = config.get('default_image', 'drone_2.png')
        fallback_radius = config.get('fallback_radius', 15.0)

        try:
            # Load the primary image
            original_image = AssetLoader.get_image(self.image_name)
            # Scale the image to fit the cell size
            self.image = pygame.transform.scale(original_image, self.grid.cell_size)
        except Exception as e:
            self.logger.warning(
                f"Failed to load image '{self.image_name}' for drone '{self.id}'. Using a placeholder. Error: {e}"
            )
            # Create a magenta placeholder surface if image fails to load
            placeholder_size = (int(self.grid.cell_size[0] * 0.8), int(self.grid.cell_size[1] * 0.8))
            self.image = pygame.Surface(placeholder_size)
            self.image.fill((255, 0, 255))  # Magenta color
        
        self.rect = self.image.get_rect()
        self.logger.info(f"Drone '{self.id}' initialized at grid_pos {list(self.position)}.")

    def move(self, direction_intent: Vector2):
        """
        Sets the drone's velocity based on a direction intent vector.
        The direction_intent should be a normalized vector.
        """
        self.velocity = direction_intent * self.speed

    def update(self, dt: float):
        """
        Updates the drone's state. Called once per frame.
        
        Args:
            dt (float): Delta time, the time elapsed since the last frame in seconds.
        """
        # Update position based on velocity and delta time
        self.position += self.velocity * dt
        
        # Update the rect for rendering
        pixel_pos = self.grid.grid_to_pixel(self.position)
        self.rect.center = pixel_pos

    def draw(self, surface: pygame.Surface, camera_offset: Vector2):
        """
        Draws the drone on the given surface, adjusted by the camera offset.
        
        Args:
            surface (pygame.Surface): The surface to draw on (usually the screen).
            camera_offset (Vector2): The offset calculated by the camera.
        """
        # Adjust the drone's rect position by the camera offset for rendering
        draw_rect = self.rect.move(-camera_offset)
        surface.blit(self.image, draw_rect)
