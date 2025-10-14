# ============================================================
#  File: asset_loader.py
#  Layer: L0-Presentation
#  Author: Reza & AI Assistant | 2025-10-13
# ============================================================

import pygame
import os
import logging
from typing import Dict, Optional, Tuple

class AssetLoader:
    """
    کلاسی برای مدیریت، بارگذاری و کش کردن منابع (assets) مانند تصاویر و فونت‌ها.
    این کار از بارگذاری مکرر فایل‌ها از دیسک جلوگیری کرده و عملکرد را بهبود می‌بخشد.
    """
    def __init__(self, base_path: str):
        """
        سازنده کلاس AssetLoader.

        Args:
            base_path (str): مسیر پوشه اصلی assets.
        """
        self.base_path = base_path
        self.image_path = os.path.join(base_path, 'images')
        self.font_path = os.path.join(base_path, 'fonts')
        
        self._image_cache: Dict[str, pygame.Surface] = {}
        self._font_cache: Dict[Tuple[str, int], pygame.font.Font] = {}
        
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.logger.info(f"AssetLoader initialized with base path: {self.base_path}")

    def get_image(self, filename: str, scale: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
        """
        یک تصویر را بارگذاری کرده و در صورت نیاز مقیاس آن را تغییر می‌دهد.
        تصاویر بارگذاری شده برای استفاده‌های بعدی کش می‌شوند.

        Args:
            filename (str): نام فایل تصویر.
            scale (Optional[Tuple[int, int]]): اندازه جدید (عرض، ارتفاع) برای تصویر.

        Returns:
            Optional[pygame.Surface]: شیء تصویر بارگذاری شده یا None در صورت بروز خطا.
        """
        cache_key = filename
        if cache_key in self._image_cache:
            img = self._image_cache[cache_key]
        else:
            full_path = os.path.join(self.image_path, filename)
            try:
                img = pygame.image.load(full_path).convert_alpha()
                self._image_cache[cache_key] = img
            except pygame.error as e:
                self.logger.error(f"Failed to load image '{full_path}': {e}")
                return None
        
        if scale:
            try:
                return pygame.transform.smoothscale(img, scale)
            except Exception as e:
                self.logger.error(f"Failed to scale image '{filename}' to {scale}: {e}")
                return img
        
        return img

    def get_font(self, filename: str, size: int) -> Optional[pygame.font.Font]:
        """
        یک فونت را با اندازه مشخص بارگذاری می‌کند.
        فونت‌های بارگذاری شده برای استفاده‌های بعدی کش می‌شوند.

        Args:
            filename (str): نام فایل فونت.
            size (int): اندازه فونت.

        Returns:
            Optional[pygame.font.Font]: شیء فونت بارگذاری شده یا None در صورت بروز خطا.
        """
        cache_key = (filename, size)
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]
        
        full_path = os.path.join(self.font_path, filename)
        try:
            font = pygame.font.Font(full_path, size)
            self._font_cache[cache_key] = font
            return font
        except pygame.error as e:
            self.logger.error(f"Failed to load font '{full_path}' with size {size}: {e}")
            return None
        except FileNotFoundError:
            self.logger.error(f"Font file not found: '{full_path}'")
            try:
                default_font = pygame.font.SysFont('Arial', size)
                self.logger.warning(f"Using system default font 'Arial' as a fallback.")
                self._font_cache[cache_key] = default_font
                return default_font
            except Exception as e_sys:
                 self.logger.error(f"Could not even load system default font: {e_sys}")
                 return None
