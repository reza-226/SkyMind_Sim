# skymind_sim/core/obstacles.py

import numpy as np

class BoxObstacle:
    """یک مانع مکعبی شکل در محیط را نمایش می‌دهد."""
    def __init__(self, min_corner, max_corner):
        """
        Args:
            min_corner (list or np.ndarray): گوشه با حداقل مختصات [x, y, z].
            max_corner (list or np.ndarray): گوشه با حداکثر مختصات [x, y, z].
        """
        self.min_corner = np.array(min_corner)
        self.max_corner = np.array(max_corner)

    def is_colliding(self, point):
        """
        بررسی می‌کند که آیا نقطه داده شده داخل این مانع قرار دارد یا خیر.
        
        Args:
            point (list or np.ndarray): نقطه‌ای که باید بررسی شود [x, y, z].
            
        Returns:
            bool: True اگر نقطه داخل مانع باشد، در غیر این صورت False.
        """
        point_arr = np.array(point)
        # np.all چک می‌کند که آیا شرط برای تمام عناصر (x, y, z) برقرار است یا نه
        return np.all(point_arr >= self.min_corner) and np.all(point_arr <= self.max_corner)
