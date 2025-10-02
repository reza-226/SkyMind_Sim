# skymind_sim/layer_1_simulation/world/obstacle.py

import pygame
from typing import Tuple

class Obstacle:
    """
    Represents a static obstacle in the simulation world.
    Now includes a pygame.Rect for easier geometric calculations.
    """
    def __init__(self, obstacle_id: str, position: Tuple[int, int], size: Tuple[int, int]):
        self.id = obstacle_id
        self.position = position
        self.size = size
        
        # --- تغییر اصلی: اضافه کردن pygame.Rect ---
        # یک شیء Rect برای محاسبات آسان‌تر (مانند تشخیص برخورد و محدوده) ایجاد می‌کنیم.
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        
        # این پیام لاگ را حذف می‌کنیم تا خروجی تمیزتر باشد.
        # print(f"Obstacle '{self.id}' created at position {self.position} with size {self.size}.")

    def get_state(self) -> dict:
        """
        Returns a serializable dictionary representing the obstacle's state.
        """
        return {
            "id": self.id,
            "position": self.position,
            "size": self.size,
            # می‌توانیم rect را هم برای نمایش اضافه کنیم اگر نیاز شد
            "rect": [self.rect.x, self.rect.y, self.rect.w, self.rect.h]
        }
