# ============================================================
#  File: obstacle.py
#  Layer: L1 - Simulation / World
#  Author: Reza & AI Assistant | 2025-10-13
# ============================================================

from typing import Tuple

class Obstacle:
    """
    نمایانگر یک مانع ثابت در محیط شبیه‌سازی.
    موقعیت و اندازه آن را برای بررسی برخورد و نمایش ذخیره می‌کند.
    """

    def __init__(self, position: Tuple[int, int], size: Tuple[int, int], id: int = None, color: Tuple[int, int, int] = (128, 128, 128)):
        """
        سازنده کلاس مانع.

        Args:
            position (Tuple[int, int]): یک تاپل (x, y) برای گوشه بالا-چپ مانع.
            size (Tuple[int, int]): یک تاپل (width, height) برای ابعاد مانع.
            id (int, optional): شناسه منحصر به فرد مانع. Defaults to None.
            color (Tuple[int, int, int], optional): رنگ RGB برای نمایش.
        """
        self.id = id
        # ما position و size را به عنوان تاپل ذخیره می‌کنیم تا کار با آنها راحت‌تر باشد.
        self.position = tuple(position) # Ensure it's a tuple
        self.size = tuple(size)         # Ensure it's a tuple
        self.color = color

    @property
    def x(self) -> int:
        """مختصات x گوشه بالا-چپ."""
        return self.position[0]

    @property
    def y(self) -> int:
        """مختصات y گوشه بالا-چپ."""
        return self.position[1]

    @property
    def width(self) -> int:
        """عرض مانع."""
        return self.size[0]

    @property
    def height(self) -> int:
        """ارتفاع مانع."""
        return self.size[1]

    def get_rect(self) -> Tuple[int, int, int, int]:
        """
        یک تاپل (x, y, width, height) برای استفاده در Pygame برمی‌گرداند.
        """
        return (self.x, self.y, self.width, self.height)

    def __repr__(self) -> str:
        return f"Obstacle(id={self.id}, position={self.position}, size={self.size})"
