# skymind_sim/core/drone.py

import numpy as np

class Drone:
    """
    نمایانگر یک پهپاد در شبیه‌سازی است.
    """
    def __init__(self, drone_id, start_position, goal_position, max_speed=5.0):
        self.id = drone_id
        self.position = np.array(start_position, dtype=float)
        self.start_position = np.array(start_position, dtype=float)
        self.goal_position = np.array(goal_position, dtype=float)
        self.max_speed = max_speed
        self.velocity = np.zeros(3, dtype=float)
        self.path = None # مسیری که باید دنبال شود (در آینده استفاده می‌شود)

    def set_path(self, path):
        """
        مسیر محاسبه شده توسط PathPlanner را برای پهپاد تنظیم می‌کند.
        """
        self.path = path

    def update(self, dt, obstacles):
        """
        موقعیت پهپاد را بر اساس گام زمانی dt به‌روز می‌کند.
        Args:
            dt (float): گام زمانی (delta time).
            obstacles (list): لیستی از آبجکت‌های موانع در محیط.
        """
        # در این نسخه ساده، پهپاد با سرعت ثابت به سمت هدف حرکت می‌کند.
        direction = self.goal_position - self.position
        distance = np.linalg.norm(direction)

        if distance > 1.0: # یک آستانه کوچک برای جلوگیری از لرزش در مقصد
            self.velocity = (direction / distance) * self.max_speed
            self.position += self.velocity * dt
        else:
            self.velocity = np.zeros(3) # رسیدن به هدف

        # TODO: در آینده باید بررسی برخورد با 'obstacles' در اینجا اضافه شود.

    # --- متد جدید که اضافه شده است ---
    def get_history_point(self):
        """
        موقعیت فعلی پهپاد را برای ثبت در تاریخچه مسیر برمی‌گرداند.
        """
        return self.position.copy()
    # --------------------------------

    def __repr__(self):
        return f"Drone(id={self.id}, pos={self.position})"
