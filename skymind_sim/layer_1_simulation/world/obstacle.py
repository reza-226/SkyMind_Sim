# skymind_sim/core/obstacle.py

import numpy as np

class Obstacle:
    """کلاس پایه برای همه موانع در محیط شبیه‌سازی."""
    def is_inside(self, point):
        """
        بررسی می‌کند که آیا یک نقطه در داخل مانع قرار دارد یا خیر.
        این متد باید در کلاس‌های فرزند پیاده‌سازی شود.
        """
        raise NotImplementedError

class BoxObstacle(Obstacle):
    """
    یک مانع مکعبی شکل را نشان می‌دهد که با مرکز، ابعاد و چرخش آن تعریف می‌شود.
    این کلاس به گونه‌ای طراحی شده که انعطاف‌پذیر باشد و بتواند از منابع داده مختلف
    (مانند فایل‌های JSON با کلیدهای 'center' یا 'position') نمونه‌سازی شود.
    """
    def __init__(self, center=None, size=None, rotation=0, **kwargs):
        """
        سازنده انعطاف‌پذیر برای مانع مکعبی.

        Args:
            center (list or np.array, optional): مختصات مرکز مکعب [x, y, z].
            size (list or np.array, optional): ابعاد مکعب [width, height, depth].
            rotation (float, optional): چرخش مانع حول محور z.
            **kwargs: پارامترهای اضافی که برای سازگاری پذیرفته و نادیده گرفته می‌شوند.
                      این شامل 'position' و 'type' می‌شود.
        """
        # برای سازگاری با فایل‌های JSON که از 'position' استفاده می‌کنند.
        # اگر 'center' داده نشده باشد، از 'position' در kwargs استفاده کن.
        final_center = center if center is not None else kwargs.get('position')
        
        if final_center is None:
            raise ValueError("BoxObstacle requires 'center' or 'position' to be specified.")
        if size is None:
            raise ValueError("BoxObstacle requires 'size' to be specified.")

        self.center = np.array(final_center, dtype=float)
        self.size = np.array(size, dtype=float)
        self.rotation = rotation

    def is_inside(self, point):
        """
        بررسی می‌کند که آیا یک نقطه داده شده در داخل این مانع مکعبی قرار دارد یا خیر.
        """
        point = np.array(point, dtype=float)
        half_size = self.size / 2.0
        min_corner = self.center - half_size
        max_corner = self.center + half_size
        return np.all(point >= min_corner) and np.all(point <= max_corner)

    def to_dict(self):
        """
        نمایش دیکشنری از مانع برای ذخیره‌سازی (با استفاده از کلید 'center').
        """
        return {
            'type': 'box',
            'center': self.center.tolist(),
            'size': self.size.tolist(),
            'rotation': self.rotation
        }

    @classmethod
    def from_dict(cls, data):
        """
        یک نمونه BoxObstacle از یک دیکشنری ایجاد می‌کند.
        این متد به سادگی داده‌ها را به سازنده اصلی پاس می‌دهد.
        """
        return cls(**data)
