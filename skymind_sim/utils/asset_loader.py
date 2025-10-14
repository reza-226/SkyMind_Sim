# مسیر: skymind_sim/layer_0_presentation/asset_loader.py
import os
import logging
import pygame

# --- Configuration for Asset Paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
IMAGE_DIR = os.path.join(ASSETS_DIR, "images")
FONT_DIR = os.path.join(ASSETS_DIR, "fonts")

def get_asset_path(asset_type: str, filename: str) -> str:
    """
    ساخت مسیر کامل برای یک Asset بر اساس نوع و نام فایل.
    در صورت نبودن فایل، پیام WARNING و بازگشت مسیر پیش‌فرض.
    """
    if asset_type == 'image':
        path = os.path.join(IMAGE_DIR, filename)
    elif asset_type == 'font':
        path = os.path.join(FONT_DIR, filename)
    else:
        raise ValueError(f"Unknown asset type: {asset_type}")
    
    if not os.path.exists(path):
        logging.warning(f"Asset not found: {path} — using fallback.")
        # مسیر پیش‌فرض پایه برای جلوگیری از توقف
        return os.path.join(IMAGE_DIR if asset_type == 'image' else FONT_DIR,
                            "drone.png" if asset_type == 'image' else "Roboto-Regular.ttf")
    return path

def load_image(filename: str, scale=None) -> pygame.Surface:
    """
    بارگذاری تصویر با مسیر امن و اعمال شفافیت.
    """
    path = get_asset_path('image', filename)
    try:
        image = pygame.image.load(path).convert_alpha()
        if scale:
            if isinstance(scale, (int, float)):
                scale = (int(scale), int(scale))
            image = pygame.transform.scale(image, scale)
        logging.info(f"Image loaded: {filename} from {path}")
        return image
    except pygame.error as e:
        logging.warning(f"Pygame error loading image '{filename}': {e} — using blank surface.")
        return pygame.Surface((scale if isinstance(scale, tuple) else (64, 64)), pygame.SRCALPHA)

def load_font(filename: str, size: int) -> pygame.font.Font:
    """
    بارگذاری فونت با مسیر امن.
    """
    path = get_asset_path('font', filename)
    try:
        font = pygame.font.Font(path, size)
        logging.info(f"Font loaded: {filename} from {path}")
        return font
    except pygame.error as e:
        logging.warning(f"Pygame error loading font '{filename}': {e} — using default pygame font.")
        return pygame.font.SysFont(None, size)
