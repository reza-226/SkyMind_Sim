import os
import pygame

# --- Configuration for Asset Paths ---
# This robustly finds the project root directory (SkyMind_Sim)
# It assumes this file is at: SkyMind_Sim/skymind_sim/utils/asset_loader.py
# So we need to go up three levels from this file's location.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
IMAGE_DIR = os.path.join(ASSETS_DIR, "images")
FONT_DIR = os.path.join(ASSETS_DIR, "fonts")

def get_asset_path(asset_type: str, filename: str) -> str:
    """Constructs the full path to an asset."""
    if asset_type == 'image':
        path = os.path.join(IMAGE_DIR, filename)
    elif asset_type == 'font':
        path = os.path.join(FONT_DIR, filename)
    else:
        raise ValueError(f"Unknown asset type: {asset_type}")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Asset not found at path: {path}")
    return path

def load_image(filename: str, size: tuple = None) -> pygame.Surface:
    """
    Loads an image, handling transparency and optional resizing.
    """
    path = get_asset_path('image', filename)
    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error as e:
        print(f"Pygame error loading image '{filename}': {e}")
        raise

def load_font(filename: str, size: int) -> pygame.font.Font:
    """
    Loads a font file from the assets directory.
    """
    path = get_asset_path('font', filename)
    try:
        return pygame.font.Font(path, size)
    except pygame.error as e:
        print(f"Pygame error loading font '{filename}': {e}")
        raise
