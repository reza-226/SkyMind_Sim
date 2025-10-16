# skymind_sim/layer_0_presentation/asset_loader.py

import pygame
import os
from typing import Dict, Optional, Tuple

from skymind_sim.utils.log_manager import LogManager

class AssetLoader:
    """A singleton class to manage loading and accessing game assets like images and fonts."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AssetLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self, base_path: str = 'assets'):
        # Check if already initialized to prevent re-initialization
        if hasattr(self, '_initialized') and self._initialized:
            return
            
        self.logger = LogManager.get_logger(__name__)
        self.base_path = base_path
        self.images: Dict[str, pygame.Surface] = {}
        self.fonts: Dict[str, str] = {}  # Store font paths
        self._loaded_fonts: Dict[Tuple[str, int], pygame.font.Font] = {} # Cache for loaded font objects
        
        self.default_font = pygame.font.get_default_font()

        # --- START OF CHANGE ---
        self._load_assets() # This line was missing!
        # --- END OF CHANGE ---

        self._initialized = True
        self.logger.info(f"AssetLoader initialized with base path: '{self.base_path}'")

    def _load_assets(self):
        """Automatically load all assets from subdirectories."""
        image_path = os.path.join(self.base_path, 'images')
        font_path = os.path.join(self.base_path, 'fonts')

        # Load images
        if os.path.isdir(image_path):
            for filename in os.listdir(image_path):
                name, ext = os.path.splitext(filename)
                if ext.lower() in ['.png', '.jpg', '.jpeg', '.bmp']:
                    full_path = os.path.join(image_path, filename)
                    try:
                        self.images[name] = pygame.image.load(full_path).convert_alpha()
                        self.logger.info(f"Loaded image: '{name}' from {full_path}")
                    except pygame.error as e:
                        self.logger.error(f"Failed to load image {full_path}: {e}")

        # Load font paths
        if os.path.isdir(font_path):
            for filename in os.listdir(font_path):
                name, ext = os.path.splitext(filename)
                if ext.lower() in ['.ttf', '.otf']:
                    full_path = os.path.join(font_path, filename)
                    self.fonts[name] = full_path
                    self.logger.info(f"Registered font: '{name}' from {full_path}")

    def get_image(self, name: str) -> pygame.Surface:
        """Retrieves a pre-loaded image by its name (filename without extension)."""
        if name not in self.images:
            self.logger.warning(f"Attempted to get non-existent image '{name}'")
            # Return a placeholder surface to avoid crashes
            placeholder = pygame.Surface((50, 50))
            placeholder.fill((255, 0, 255)) # Bright pink to indicate missing texture
            return placeholder
        return self.images[name]

    def get_font(self, name: str, size: int) -> pygame.font.Font:
        """Retrieves a font object by name and size, loading it if not already cached."""
        font_key = (name, size)
        if font_key in self._loaded_fonts:
            return self._loaded_fonts[font_key]

        if name in self.fonts:
            try:
                font = pygame.font.Font(self.fonts[name], size)
                self._loaded_fonts[font_key] = font
                return font
            except pygame.error as e:
                self.logger.error(f"Could not load font '{name}' at size {size}: {e}")
        
        self.logger.warning(f"Attempted to get non-existent font '{name}' with size {size}. Falling back to default.")
        font = pygame.font.Font(self.default_font, size)
        self._loaded_fonts[font_key] = font # Cache the default font as well
        return font
