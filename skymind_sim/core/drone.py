# skymind_sim/core/drone.py

import numpy as np
from typing import Optional, List

class Drone:
    """
    کلاسی برای نمایش یک پهپاد در شبیه‌سازی.
    این پهپاد اکنون از یک مسیریاب برای رسیدن به هدف استفاده می‌کند.
    """
    _id_counter = 0

    def __init__(self, start_pos: np.ndarray, goal_pos: np.ndarray, velocity: float = 5.0, size: float = 0.5):
        """
        سازنده کلاس Drone.

        Args:
            start_pos (np.ndarray): موقعیت شروع پهپاد.
            goal_pos (np.ndarray): موقعیت هدف نهایی پهپاد.
            velocity (float): سرعت حرکت پهپاد (متر بر ثانیه).
            size (float): اندازه (شعاع) پهپاد برای تشخیص برخورد.
        """
        self.id = Drone._id_counter
        Drone._id_counter += 1

        self.position = np.array(start_pos, dtype=float)
        self.goal_pos = np.array(goal_pos, dtype=float)
        self.velocity = velocity
        self.size = size
        
        self.path: Optional[List[np.ndarray]] = None
        self.current_path_index = 0
        self.environment = None
        self.state = "IDLE"  # وضعیت‌ها: IDLE, PLANNING, MOVING, FINISHED

    def set_environment(self, environment):
        """
        محیط را برای پهپاد تنظیم کرده و فرآیند مسیریابی را آغاز می‌کند.
        """
        self.environment = environment
        self.plan_path()

    def plan_path(self):
        """
        از مسیریاب محیط برای یافتن مسیر به سمت هدف استفاده می‌کند.
        """
        if self.environment and self.environment.path_planner:
            print(f"Drone {self.id}: Planning path from {self.position} to {self.goal_pos}...")
            self.state = "PLANNING"
            self.path = self.environment.path_planner.find_path(self.position, self.goal_pos)
            
            if self.path:
                print(f"Drone {self.id}: Path found with {len(self.path)} waypoints.")
                self.current_path_index = 0
                self.state = "MOVING"
            else:
                print(f"Drone {self.id}: Failed to find a path.")
                self.state = "IDLE" # یا "FAILED"

    def update(self, dt: float):
        """
        موقعیت پهپاد را بر اساس مسیر محاسبه‌شده به‌روزرسانی می‌کند.
        """
        if self.state != "MOVING" or not self.path:
            return

        # اگر به آخرین نقطه مسیر رسیده‌ایم
        if self.current_path_index >= len(self.path):
            self.state = "FINISHED"
            print(f"Drone {self.id} has reached its destination.")
            return

        # استخراج نقطه هدف بعدی در مسیر
        target_waypoint = self.path[self.current_path_index]
        
        direction_vector = target_waypoint - self.position
        distance_to_target = np.linalg.norm(direction_vector)

        # اگر فاصله تا نقطه بعدی خیلی کم است، به نقطه بعدی در مسیر بروید
        if distance_to_target < 0.1: # یک آستانه کوچک برای جلوگیری از لرزش
            self.current_path_index += 1
            return

        # محاسبه حرکت در این فریم زمانی
        move_distance = self.velocity * dt
        
        # اگر فاصله تا هدف کمتر از مسافت حرکت است، مستقیم به هدف بروید
        if move_distance >= distance_to_target:
            self.position = target_waypoint
            self.current_path_index += 1
        else:
            # در غیر این صورت، در جهت هدف حرکت کنید
            normalized_direction = direction_vector / distance_to_target
            self.position += normalized_direction * move_distance

    def get_history_point(self):
        """برای رسم مسیر طی شده استفاده می‌شود."""
        return self.position.copy()
