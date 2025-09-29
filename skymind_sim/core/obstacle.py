# skymind_sim/core/obstacle.py

import numpy as np

class Obstacle:
    """
    کلاسی برای نمایش یک مانع کروی در محیط شبیه‌سازی.
    
    این کلاس یک مانع را با استفاده از یک نقطه مرکزی و یک شعاع تعریف می‌کند.
    این مدل ساده برای محاسبات تشخیص برخورد بسیار کارآمد است.

    Attributes:
        center (np.ndarray): یک آرایه NumPy با ابعاد (3,) که مختصات [x, y, z] مرکز کره را نگه می‌دارد.
        radius (float): شعاع مانع کروی.
    """
    def __init__(self, center: np.ndarray, radius: float):
        """
        سازنده کلاس Obstacle.

        Args:
            center (np.ndarray): مختصات مرکز مانع به صورت [x, y, z].
                                 توصیه می‌شود که از نوع np.ndarray با dtype=float باشد.
            radius (float): شعاع مانع. باید یک عدد مثبت باشد.
        """
        # بررسی می‌کنیم که مرکز یک آرایه NumPy با 3 عنصر باشد
        if not isinstance(center, np.ndarray) or center.shape != (3,):
            raise ValueError("مرکز مانع (center) باید یک آرایه NumPy با ابعاد (3,) باشد.")
        
        # بررسی می‌کنیم که شعاع یک عدد مثبت باشد
        if not isinstance(radius, (int, float)) or radius <= 0:
            raise ValueError("شعاع (radius) باید یک عدد مثبت باشد.")

        self.center = center.astype(float)  # اطمینان از اینکه داده‌ها از نوع float هستند
        self.radius = float(radius)

    def __repr__(self) -> str:
        """
        نمایش رشته‌ای خوانا از شیء برای دیباگ کردن.
        """
        # np.array2string برای نمایش زیباتر آرایه NumPy استفاده می‌شود
        center_str = np.array2string(self.center, precision=2, separator=', ')
        return f"Obstacle(center={center_str}, radius={self.radius:.2f})"

    def is_colliding(self, point: np.ndarray) -> bool:
        """
        بررسی می‌کند که آیا یک نقطه مشخص با این مانع برخورد دارد یا خیر.
        
        یک نقطه زمانی با یک مانع کروی برخورد می‌کند که فاصله آن از مرکز کره
        کمتر یا مساوی شعاع کره باشد.

        Args:
            point (np.ndarray): مختصات [x, y, z] نقطه‌ای که می‌خواهیم بررسی کنیم.

        Returns:
            bool: اگر نقطه داخل یا روی سطح مانع باشد True، در غیر این صورت False.
        """
        # محاسبه فاصله اقلیدسی بین نقطه و مرکز مانع
        distance = np.linalg.norm(point - self.center)
        
        # اگر فاصله کمتر یا مساوی شعاع بود، برخورد رخ داده است
        return distance <= self.radius
