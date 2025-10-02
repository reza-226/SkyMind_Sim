# skymind_sim/layer_1_simulation/entities/drone.py
from typing import Tuple, List, Dict, Any, Optional

class Drone:
    def __init__(self, drone_id: str, initial_position: Tuple[float, float], speed: float = 50.0):
        """
        مقداردهی اولیه پهپاد.

        Args:
            drone_id (str): شناسه منحصر به فرد پهپاد.
            initial_position (Tuple[float, float]): موقعیت اولیه (x, y) پهپاد.
            speed (float): سرعت حرکت پهپاد بر حسب پیکسل بر ثانیه.
        """
        self.id = drone_id
        self.position: Tuple[float, float] = initial_position
        self.speed: float = speed  # پیکسل بر ثانیه
        self.path: List[Tuple[float, float]] = []
        self.current_target_index: int = 0
        print(f"Drone '{self.id}' created at position {self.position}.")

    def set_path(self, path: List[Tuple[float, float]]):
        """یک مسیر برای حرکت پهپاد تنظیم می‌کند."""
        self.path = path
        self.current_target_index = 0
        if path:
            # موقعیت اولیه را به اولین نقطه مسیر به‌روزرسانی می‌کنیم
            self.position = path[0]
            self.current_target_index = 1

    def update(self, dt: float):
        """موقعیت پهپاد را بر اساس مسیر و زمان سپری شده (dt) به‌روزرسانی می‌کند."""
        if not self.path or self.current_target_index >= len(self.path):
            return  # مسیری برای دنبال کردن وجود ندارد

        target_pos = self.path[self.current_target_index]
        current_pos = self.position

        # محاسبه بردار جهت به سمت هدف
        dx = target_pos[0] - current_pos[0]
        dy = target_pos[1] - current_pos[1]
        
        # محاسبه فاصله تا هدف
        distance = (dx**2 + dy**2)**0.5

        if distance < 1.0:
            # به هدف رسیده‌ایم، به هدف بعدی می‌رویم
            self.current_target_index += 1
            if self.current_target_index >= len(self.path):
                # به انتهای مسیر رسیده‌ایم
                self.path = [] # مسیر را خالی میکنیم که پهپاد متوقف شود
            return

        # نرمال‌سازی بردار جهت
        direction_x = dx / distance
        direction_y = dy / distance

        # محاسبه مسافت قابل حرکت در این فریم
        move_distance = self.speed * dt

        # حرکت پهپاد
        new_x = current_pos[0] + direction_x * move_distance
        new_y = current_pos[1] + direction_y * move_distance
        
        self.position = (new_x, new_y)


    def get_state(self) -> Dict[str, Any]:
        """وضعیت فعلی پهپاد را برای استفاده در لایه‌های دیگر برمی‌گرداند."""
        return {
            "id": self.id,
            "position": self.position,
            "path_remaining": self.path[self.current_target_index:] if self.path else []
        }
