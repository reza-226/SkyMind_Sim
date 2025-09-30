# skymind_sim/core/drone.py

import numpy as np
from enum import Enum, auto

class DroneStatus(Enum):
    """
    وضعیت‌های مختلفی که یک پهپاد می‌تواند داشته باشد.
    """
    IDLE = auto()       # بیکار، در پایگاه
    PLANNING = auto()   # در حال محاسبه مسیر
    MOVING = auto()     # در حال حرکت در طول مسیر
    HOVERING = auto()   # شناور در یک نقطه
    LANDING = auto()    # در حال فرود
    FINISHED = auto()   # ماموریت تمام شده

class Drone:
    """
    این کلاس نمایانگر یک پهپاد در شبیه‌سازی است.
    """
    def __init__(self, drone_id, initial_position, speed=5.0):
        """
        سازنده کلاس Drone.

        Args:
            drone_id (any): شناسه منحصر به فرد برای پهپاد.
            initial_position (np.ndarray): موقعیت شروع پهپاد (x, y, z).
            speed (float): سرعت حرکت پهپاد (متر بر ثانیه).
        """
        self.id = drone_id
        self.position = np.array(initial_position, dtype=float)
        self.speed = speed
        self.status = DroneStatus.IDLE
        self.path = None
        self._path_index = 0

    def assign_path(self, path):
        """
        یک مسیر محاسبه شده را به پهپاد اختصاص می‌دهد.

        Args:
            path (list): لیستی از نقاط (مختصات) که مسیر را تشکیل می‌دهند.
        """
        if path and len(path) > 1:
            self.path = path
            self.status = DroneStatus.MOVING
            self._path_index = 1 # شروع حرکت به سمت نقطه دوم در مسیر (نقطه اول موقعیت فعلی است)
            print(f"Drone {self.id}: Path assigned. Ready to move.")
        else:
            print(f"Drone {self.id}: Invalid path assigned. Staying IDLE.")
            self.status = DroneStatus.IDLE

    def update(self, dt):
        """
        موقعیت پهپاد را بر اساس زمان سپری شده (dt) به‌روزرسانی می‌کند.

        Args:
            dt (float): گام زمانی شبیه‌سازی (دلتا تایم).
        """
        if self.status != DroneStatus.MOVING or not self.path:
            return # اگر در حال حرکت نیست، کاری انجام نده

        # اگر به انتهای مسیر رسیده‌ایم
        if self._path_index >= len(self.path):
            self.status = DroneStatus.FINISHED
            print(f"Drone {self.id}: Reached destination at {self.position.round(2)}. Mission finished.")
            return

        # استخراج نقطه هدف بعدی
        target_point = np.array(self.path[self._path_index])
        
        # محاسبه بردار جهت و فاصله تا هدف
        direction_vector = target_point - self.position
        distance_to_target = np.linalg.norm(direction_vector)
        
        # محاسبه مسافتی که در این گام زمانی می‌توان طی کرد
        travel_distance = self.speed * dt
        
        # اگر فاصله قابل طی کردن بیشتر از فاصله تا هدف بعدی است
        if travel_distance >= distance_to_target:
            # مستقیماً به نقطه هدف برو
            self.position = target_point
            # و هدف بعدی را انتخاب کن
            self._path_index += 1
            print(f"Drone {self.id}: Reached path point {self._path_index - 1} at {self.position.round(2)}")
        else:
            # در غیر این صورت، در جهت هدف حرکت کن
            normalized_direction = direction_vector / distance_to_target
            self.position += normalized_direction * travel_distance

    def __str__(self):
        """نمایش متنی وضعیت پهپاد."""
        pos_str = f"[{self.position[0]:.2f}, {self.position[1]:.2f}, {self.position[2]:.2f}]"
        return f"Drone {self.id} | Status: {self.status.name} | Position: {pos_str}"
