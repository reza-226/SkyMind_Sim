# skymind_sim/core/environment.py

from .drone import Drone
from typing import List, Tuple

class Environment:
    """
    این کلاس نمایانگر محیط شبیه‌سازی دو بعدی است.
    محیط یک اندازه مشخص دارد و می‌تواند شامل موانع و پهپادها باشد.
    """
    def __init__(self, width: int, height: int):
        """
        سازنده کلاس محیط.

        Args:
            width (int): عرض محیط (اندازه در محور x).
            height (int): ارتفاع محیط (اندازه در محور y).
        """
        if width <= 0 or height <= 0:
            raise ValueError("Environment width and height must be positive integers.")
            
        self.width: int = width
        self.height: int = height
        self.obstacles: List[Tuple[int, int]] = []  # لیستی از مختصات موانع (x, y)
        self.drones: List[Drone] = []  # لیستی از اشیاء پهپاد در محیط

    def add_drone(self, drone: Drone):
        """
        یک پهپاد جدید را به محیط اضافه می‌کند.
        بررسی می‌کند که آیا موقعیت اولیه پهپاد معتبر است یا خیر.
        """
        if not self.is_valid_position(drone.position):
            raise ValueError(f"Cannot add drone '{drone.id}' at invalid position {drone.position}.")
        
        print(f"[Environment] Adding drone '{drone.id}' at {drone.position}.")
        self.drones.append(drone)

    def add_obstacle(self, position: Tuple[int, int]):
        """ یک مانع را در یک موقعیت مشخص به محیط اضافه می‌کند. """
        if self.is_valid_position(position):
            if position not in self.obstacles:
                self.obstacles.append(position)
                print(f"[Environment] Added obstacle at {position}.")
            else:
                print(f"[Environment] Obstacle already exists at {position}.")
        else:
            print(f"[Warning] Cannot add obstacle outside of environment bounds: {position}.")


    def is_valid_position(self, position: Tuple[int, int]) -> bool:
        """
        بررسی می‌کند که آیا یک موقعیت داخل مرزهای محیط است و یک مانع نیست.
        """
        x, y = position
        # چک کردن مرزها
        within_bounds = (0 <= x < self.width) and (0 <= y < self.height)
        if not within_bounds:
            return False
        
        # چک کردن موانع
        if position in self.obstacles:
            return False
            
        return True

    def display(self):
        """
        یک نمایش متنی ساده از محیط و موقعیت پهپادها را چاپ می‌کند.
        '.' برای فضای خالی، 'D' برای پهپاد، 'X' برای مانع.
        (برای محیط‌های بزرگ مناسب نیست، اما برای تست عالی است)
        """
        print(f"\n--- Environment Display ({self.width}x{self.height}) ---")
        
        # یک دیکشنری برای دسترسی سریع به موقعیت‌ها ایجاد می‌کنیم
        drone_positions = {drone.position: drone.id for drone in self.drones}

        # برای اینکه محور y مثل نمودارهای ریاضی از پایین به بالا باشد، برعکس چاپ می‌کنیم
        for y in range(self.height - 1, -1, -1):
            row_str = f"{y:2d} | "
            for x in range(self.width):
                pos = (x, y)
                if pos in drone_positions:
                    row_str += "D " # نمایش پهپاد
                elif pos in self.obstacles:
                    row_str += "X " # نمایش مانع
                else:
                    row_str += ". " # نمایش فضای خالی
            print(row_str)
        
        # چاپ خط افقی و شماره محور x
        print("   +" + "--" * self.width)
        x_axis = "     " + " ".join([f"{i:<2}" for i in range(self.width)])
        print(x_axis)
        print("-" * 25)
