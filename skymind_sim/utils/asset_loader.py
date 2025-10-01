# skymind_sim/utils/asset_loader.py
import pygame
import os

class AssetLoader:
    _images = {}
    _initialized = False

    @staticmethod
    def load_assets():
        """
        Loads all visual assets (images) for the project.
        This method should be called once at the beginning of the program.
        """
        if AssetLoader._initialized:
            return
            
        print("INFO: Loading all assets...")
        
        # Find the path to the images folder
        base_path = os.path.dirname(__file__)
        image_dir = os.path.abspath(os.path.join(base_path, '..', '..', 'assets', 'images'))

        # Load the drone image
        try:
            drone_image_path = os.path.join(image_dir, 'drone.png')
            image = pygame.image.load(drone_image_path).convert_alpha()
            AssetLoader._images['drone'] = image
            print(f"INFO: Successfully loaded 'drone.png' from {drone_image_path}")
        except pygame.error as e:
            print(f"FATAL: Failed to load 'drone.png'. Error: {e}")
            raise

        AssetLoader._initialized = True
        print("INFO: Asset loading complete.")

    @staticmethod
    def get_image(name):
        """
        Returns a pre-loaded image by its name.

        :param name: The key name of the image (e.g., 'drone').
        :return: The pygame.Surface object of the image.
        """
        image = AssetLoader._images.get(name)
        if image is None:
            raise KeyError(f"Image with name '{name}' not found. Make sure it was loaded in load_assets().")
        return image
