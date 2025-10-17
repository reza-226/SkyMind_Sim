# skymind_sim/layer_0_presentation/camera.py

import pygame
from pygame.math import Vector2

class Camera:
    """
    Manages the viewport of the simulation, allowing the view to follow a target
    entity and stay within the bounds of the world.
    """
    def __init__(self, target, screen_width, screen_height, world_width, world_height):
        """
        Initializes the Camera.
        
        Args:
            target (object): The entity the camera should follow. Must have a 'rect' attribute.
            screen_width (int): The width of the game window in pixels.
            screen_height (int): The height of the game window in pixels.
            world_width (int): The total width of the world in pixels.
            world_height (int): The total height of the world in pixels.
        """
        self.target = target
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        
        # The offset is the top-left coordinate of the camera's view in world space.
        self.offset = Vector2(0, 0)
        self.half_w = self.screen_width // 2
        self.half_h = self.screen_height // 2

    def update(self, dt: float):
        """
        Updates the camera's offset to center on the target, clamping to world boundaries.
        
        Args:
            dt (float): Delta time, not directly used here but good practice for updates.
        """
        if self.target:
            # Center the camera on the target's position
            target_x = self.target.rect.centerx - self.half_w
            target_y = self.target.rect.centery - self.half_h
            
            # Clamp the camera's position to the world boundaries
            # The camera cannot show an area outside of the world map.
            clamped_x = max(0, min(target_x, self.world_width - self.screen_width))
            clamped_y = max(0, min(target_y, self.world_height - self.screen_height))
            
            self.offset.x = clamped_x
            self.offset.y = clamped_y

    def get_offset(self) -> Vector2:
        """Returns the current camera offset."""
        return self.offset
