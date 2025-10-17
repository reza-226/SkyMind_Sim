# skymind_sim/layer_0_presentation/asset_loader.py

import pygame
import os
import logging
from typing import Dict

class AssetLoader:
    """
    A static class responsible for loading and caching game assets like images and fonts.
    """
    _image_cache: Dict[str, pygame.Surface] = {}
    _font_cache: Dict[str, pygame.font.Font] = {}
    _assets_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
    _image_path = os.path.join(_assets_path, 'images')
    _font_path = os.path.join(_assets_path, 'fonts')

    @staticmethod
    def _load_image(name: str) -> pygame.Surface:
        """Loads an image file into a pygame.Surface."""
        logger = logging.getLogger(__name__)
        full_path = os.path.join(AssetLoader._image_path, name)
        try:
            image = pygame.image.load(full_path)
            # Convert alpha for better blitting performance
            if image.get_alpha():
                image = image.convert_alpha()
            else:
                image = image.convert()
            logger.info(f"Successfully loaded image: {name}")
            return image
        except pygame.error as e:
            logger.error(f"Cannot load image: {name} from path {full_path}. Error: {e}")
            raise

    # --- THIS IS THE FIX ---
    @staticmethod
    # -----------------------
    def get_image(name: str) -> pygame.Surface:
        """
        Retrieves a cached image or loads it if it's not in the cache.
        
        Args:
            name (str): The filename of the image in the assets/images folder.

        Returns:
            pygame.Surface: The loaded image surface.
        """
        if name not in AssetLoader._image_cache:
            AssetLoader._image_cache[name] = AssetLoader._load_image(name)
        return AssetLoader._image_cache[name]

    @staticmethod
    def get_font(name: str, size: int) -> pygame.font.Font:
        """
        Retrieves a cached font or loads it if it's not in the cache.
        
        Args:
            name (str): The filename of the font in the assets/fonts folder.
            size (int): The desired font size.

        Returns:
            pygame.font.Font: The loaded font object.
        """
        key = f"{name}_{size}"
        if key not in AssetLoader._font_cache:
            full_path = os.path.join(AssetLoader._font_path, name)
            try:
                AssetLoader._font_cache[key] = pygame.font.Font(full_path, size)
                logging.getLogger(__name__).info(f"Successfully loaded font: {name} with size {size}")
            except pygame.error as e:
                logging.getLogger(__name__).error(f"Cannot load font: {name}. Using default. Error: {e}")
                AssetLoader._font_cache[key] = pygame.font.Font(None, size) # Fallback to default font
        return AssetLoader._font_cache[key]
