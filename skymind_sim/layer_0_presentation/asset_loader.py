# skymind_sim/layer_0_presentation/asset_loader.py

import pygame
import os
import logging

logger = logging.getLogger(__name__)

# --- بخش اصلاح شده برای محاسبه مسیر ریشه پروژه ---
# این کد به صورت قابل اعتمادتری مسیر ریشه پروژه را پیدا می‌کند.
# فرض بر این است که این فایل در skymind_sim/layer_0_presentation/ قرار دارد.
# بنابراین، با دو بار بازگشت به عقب (os.path.dirname), به ریشه پروژه می‌رسیم.
try:
    CURRENT_FILE_PATH = os.path.abspath(__file__)
    LAYER_0_DIR = os.path.dirname(CURRENT_FILE_PATH)
    SKYBIND_SIM_DIR = os.path.dirname(LAYER_0_DIR)
    PROJECT_ROOT = os.path.dirname(SKYBIND_SIM_DIR)
except NameError:
    # __file__ ممکن است در برخی محیط‌ها (مانند REPL تعاملی) تعریف نشده باشد
    # در این حالت از مسیر کاری فعلی به عنوان یک جایگزین استفاده می‌کنیم
    PROJECT_ROOT = os.getcwd()

ASSETS_DIR = os.path.join(PROJECT_ROOT, 'assets')
# --------------------------------------------------


class AssetLoader:
    """
    A Singleton class to handle loading of assets like images and fonts.
    This ensures that assets are loaded only once by caching them.
    """
    _instance = None
    _cache = {}

    def __new__(cls):
        if cls._instance is None:
            logger.info("AssetLoader Singleton Initialized.")
            cls._instance = super(AssetLoader, cls).__new__(cls)
            cls._instance._cache = {}  # Initialize cache for the instance
        return cls._instance

    def load_image(self, filename: str):
        """
        Loads an image from the 'assets/images' directory.
        Uses a cache to avoid reloading the same image.

        Args:
            filename (str): The name of the image file.

        Returns:
            pygame.Surface: The loaded image surface.
        """
        if filename in self._cache:
            return self._cache[filename]
            
        path = os.path.join(ASSETS_DIR, 'images', filename)
        try:
            image = pygame.image.load(path).convert_alpha()
            self._cache[filename] = image
            logger.debug(f"Loaded image '{filename}' and cached it.")
            return image
        except pygame.error as e:
            # لاگ کردن مسیر کامل برای دیباگینگ آسان‌تر
            full_path = os.path.abspath(path)
            logger.error(f"Error loading image. Attempted to load from path: '{full_path}'. Error: {e}")
            raise

    def load_font(self, filename: str, size: int):
        """
        Loads a font from the 'assets/fonts' directory.
        Uses a cache to avoid reloading the same font at the same size.

        Args:
            filename (str): The name of the font file.
            size (int): The desired font size.

        Returns:
            pygame.font.Font: The loaded font object.
        """
        cache_key = f"{filename}_{size}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        path = os.path.join(ASSETS_DIR, 'fonts', filename)
        try:
            font = pygame.font.Font(path, size)
            self._cache[cache_key] = font
            logger.debug(f"Loaded font '{filename}' with size {size} and cached it.")
            return font
        except pygame.error as e:
            # لاگ کردن مسیر کامل برای دیباگینگ آسان‌تر
            full_path = os.path.abspath(path)
            logger.error(f"Error loading font. Attempted to load from path: '{full_path}'. Error: {e}")
            raise
