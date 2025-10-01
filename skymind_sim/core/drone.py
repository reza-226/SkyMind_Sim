# skymind_sim/core/drone.py
import pygame
from ..utils.asset_loader import AssetLoader

class Drone(pygame.sprite.Sprite):
    def __init__(self, start_pos=(0, 0)):
        """
        Initializes the Drone object.

        :param start_pos: A tuple (x, y) for the initial position.
        """
        super().__init__()
        
        print("INFO: Initializing Drone...")
        
        # Get the drone image from the AssetLoader
        self.image = AssetLoader.get_image('drone')
        
        # Get the rect and set its position
        self.rect = self.image.get_rect(center=start_pos)
        
        print(f"INFO: Drone created at position: {self.rect.center}")
