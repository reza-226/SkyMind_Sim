# skymind_sim/core/drone.py

import numpy as np

class Drone:
    """
    نمایانگر یک پهپاد در شبیه‌سازی است.

    Attributes:
        drone_id (str): شناسه منحصر به فرد پهپاد.
        position (np.ndarray): موقعیت فعلی پهپاد در فضای سه‌بعدی [x, y, z].
        initial_position (np.ndarray): موقعیت شروع پهپاد.
        speed (float): سرعت حرکت پهپاد (متر بر ثانیه).
        movement_path (list): لیستی از نقاط مقصد (np.ndarray) که پهپاد باید طی کند.
        current_target_index (int): اندیس هدف فعلی در movement_path.
    """
    def __init__(self, drone_id: str, initial_position: np.ndarray, speed: float = 20.0):
        """
        سازنده کلاس Drone.

        Args:
            drone_id (str): شناسه منحصر به فرد برای پهپاد.
            initial_position (np.ndarray): مختصات موقعیت اولیه [x, y, z].
            speed (float): سرعت پهپاد بر حسب متر بر ثانیه. پیش‌فرض 20.0 است.
        """
        if not isinstance(drone_id, str) or not drone_id:
            raise ValueError("drone_id باید یک رشته غیرخالی باشد.")
        if not isinstance(initial_position, np.ndarray) or initial_position.shape != (3,):
            raise ValueError("initial_position باید یک آرایه NumPy با سه عنصر باشد.")
        if not isinstance(speed, (int, float)) or speed <= 0:
            raise ValueError("speed باید یک عدد مثبت باشد.")

        self._drone_id = drone_id
        self._initial_position = initial_position.copy()
        self._position = initial_position.copy()
        self._speed = speed
        self._movement_path = []
        self._current_target_index = 0

    @property
    def drone_id(self) -> str:
        return self._drone_id

    @property
    def position(self) -> np.ndarray:
        return self._position

    @property
    def initial_position(self) -> np.ndarray:
        return self._initial_position

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def movement_path(self) -> list:
        return self._movement_path

    def set_movement_path(self, path: list):
        """
        یک مسیر حرکتی برای پهپاد تنظیم می‌کند.
        
        Args:
            path (list): لیستی از آرایه‌های NumPy که هر کدام یک نقطه مقصد هستند.
        """
        if not isinstance(path, list) or not all(isinstance(p, np.ndarray) and p.shape == (3,) for p in path):
            raise ValueError("مسیر باید لیستی از آرایه‌های NumPy سه‌بعدی باشد.")
        self._movement_path = path
        self._current_target_index = 0

    def move(self, delta_time: float):
        """
        پهپاد را برای یک گام زمانی به سمت هدف بعدی حرکت می‌دهد.
        
        Args:
            delta_time (float): زمان سپری شده از آخرین حرکت (بر حسب ثانیه).
        """
        if not self._movement_path:
            return  # اگر مسیری تعریف نشده باشد، حرکتی نکن

        target_position = self._movement_path[self._current_target_index]
        direction_vector = target_position - self._position
        distance_to_target = np.linalg.norm(direction_vector)

        if distance_to_target < 1e-6:  # اگر به هدف رسیده‌ایم
            self._current_target_index = (self._current_target_index + 1) % len(self._movement_path)
            return

        travel_distance = self._speed * delta_time

        if travel_distance >= distance_to_target:
            self._position = target_position.copy()
            self._current_target_index = (self._current_target_index + 1) % len(self._movement_path)
        else:
            self._position += (direction_vector / distance_to_target) * travel_distance

    def __repr__(self) -> str:
        return f"Drone(id='{self.drone_id}', position={np.round(self.position, 2)})"
