# skymind_sim/core/obstacle.py

import numpy as np

class Obstacle:
    """
    یک مانع مکعبی شکل در محیط را تعریف می‌کند.
    
    این مانع با دو نقطه تعریف می‌شود: گوشه با حداقل مختصات (min_corner)
    و گوشه با حداکثر مختصات (max_corner).
    
    Attributes:
        min_corner (np.ndarray): مختصات [x_min, y_min, z_min] مانع.
        max_corner (np.ndarray): مختصات [x_max, y_max, z_max] مانع.
        center (np.ndarray): مرکز هندسی مانع.
    """
    def __init__(self, min_corner: list[float] | np.ndarray, max_corner: list[float] | np.ndarray):
        """
        یک مانع مکعبی را مقداردهی اولیه می‌کند.
        
        Args:
            min_corner: گوشه‌ای از مکعب با کمترین مقادیر x, y, z.
            max_corner: گوشه‌ای از مکعب با بیشترین مقادیر x, y, z.
        """
        self.min_corner = np.array(min_corner, dtype=float)
        self.max_corner = np.array(max_corner, dtype=float)
        
        if np.any(self.min_corner >= self.max_corner):
            raise ValueError("min_corner must be strictly less than max_corner in all dimensions.")
            
        self.center = (self.min_corner + self.max_corner) / 2.0

    def check_collision(self, point: np.ndarray) -> bool:
        """
        بررسی می‌کند که آیا یک نقطه مشخص با این مانع برخورد دارد یا خیر.
        
        Args:
            point (np.ndarray): نقطه‌ای که باید بررسی شود.
            
        Returns:
            bool: True اگر نقطه داخل مانع باشد، در غیر این صورت False.
        """
        # A point is inside the cube if for all axes (x, y, z),
        # its coordinate is between min_corner and max_corner.
        is_inside = np.all((point >= self.min_corner) & (point <= self.max_corner))
        return is_inside
