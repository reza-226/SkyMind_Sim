# skymind_sim/layer_1_simulation/world/obstacle.py
from typing import Tuple, Dict, Any

class Obstacle:
    def __init__(self, obstacle_id: str, position: Tuple[float, float], size: Tuple[float, float]):
        """
        مقداردهی اولیه یک مانع.

        Args:
            obstacle_id (str): شناسه منحصر به فرد مانع.
            position (Tuple[float, float]): موقعیت گوشه بالا-چپ (x, y) مانع.
            size (Tuple[float, float]): ابعاد (width, height) مانع.
        """
        self.id = obstacle_id
        self.position = position
        self.size = size
        print(f"Obstacle '{self.id}' created at position {self.position} with size {self.size}.")


    def get_state(self) -> Dict[str, Any]:
        """وضعیت مانع را برای لایه‌های دیگر برمی‌گرداند."""
        return {
            "id": self.id,
            "position": self.position,
            "size": self.size
        }
