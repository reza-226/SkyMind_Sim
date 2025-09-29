# skymind_sim/core/environment.py

import json
import numpy as np
from .drone import Drone
from .obstacles import BoxObstacle # اطمینان از ایمپورت صحیح

class Environment:
    """
    این کلاس محیط شبیه‌سازی را مدیریت می‌کند که شامل ابعاد، موانع و پهپادها است.
    """
    def __init__(self, dimensions, obstacles, drones):
        self.dimensions = np.array(dimensions, dtype=float)
        self.obstacles = obstacles if obstacles is not None else []
        self.drones = drones if drones is not None else []

    @classmethod
    def from_json_file(cls, file_path):
        """
        یک آبجکت Environment از روی یک فایل JSON ایجاد می‌کند.
        """
        print(f"Loading map from '{file_path}'...")
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading or parsing map file: {e}")
            return None

        # استخراج ابعاد محیط
        dimensions = data.get("dimensions", [100, 100, 50])

        # استخراج و ساخت آبجکت‌های موانع
        obstacles = []
        for obs_data in data.get("obstacles", []):
            if obs_data.get("type") == "box":
                obstacle = BoxObstacle(
                    min_corner=obs_data["min_corner"],
                    max_corner=obs_data["max_corner"]
                )
                obstacles.append(obstacle)
        
        # استخراج و ساخت آبجکت‌های پهپادها
        drones = []
        for drone_data in data.get("drones", []):
            drone = Drone(
                drone_id=drone_data["id"],
                start_position=drone_data["start"],
                goal_position=drone_data["goal"]
            )
            drones.append(drone)

        # فراخوانی سازنده اصلی کلاس با داده‌های استخراج شده
        return cls(dimensions=dimensions, obstacles=obstacles, drones=drones)

    # --- متد جدید که اضافه شده است ---
    def update(self, dt):
        """
        وضعیت تمام اجزای محیط را برای یک گام زمانی dt به‌روز می‌کند.
        Args:
            dt (float): گام زمانی (delta time) بر حسب ثانیه.
        """
        # در حال حاضر، فقط وضعیت پهپادها را به‌روز می‌کنیم.
        for drone in self.drones:
            drone.update(dt, self.obstacles)
    # --------------------------------
