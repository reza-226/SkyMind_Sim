# skymind_sim/core/drone.py

# در آینده ممکن است برای کار با مختصات به کتابخانه‌هایی مثل NumPy نیاز پیدا کنیم.
# import numpy as np

class Drone:
    """
    این کلاس نمایانگر یک پهپاد در محیط شبیه‌سازی است.

    هر پهپاد دارای یک شناسه، موقعیت، وضعیت و سطح باتری است.
    """

    def __init__(self, drone_id: str, start_position: tuple[int, int], battery_level: float = 100.0):
        """
        سازنده (Constructor) کلاس پهپاد.

        Args:
            drone_id (str): شناسه منحصر به فرد پهپاد.
            start_position (tuple[int, int]): موقعیت اولیه پهپاد به صورت (x, y).
            battery_level (float, optional): سطح اولیه باتری. پیش‌فرض 100.0 است.
        """
        if not isinstance(drone_id, str) or not drone_id:
            raise ValueError("Drone ID must be a non-empty string.")
        
        if not (isinstance(start_position, tuple) and len(start_position) == 2 and
                all(isinstance(i, int) for i in start_position)):
            raise ValueError("Start position must be a tuple of two integers (x, y).")

        self.id: str = drone_id
        self.position: tuple[int, int] = start_position
        self.battery_level: float = float(battery_level)
        self.status: str = "IDLE"  # وضعیت‌های ممکن: IDLE, FLYING, RETURNING, CHARGING

    def __str__(self) -> str:
        """
        نمایش متنی خوانا از شیء پهپاد.
        وقتی از print(my_drone) استفاده می‌کنید، این متد فراخوانی می‌شود.
        """
        return f"Drone(ID='{self.id}', Position={self.position}, Status='{self.status}', Battery={self.battery_level:.1f}%)"

    def __repr__(self) -> str:
        """
        نمایش رسمی شیء، که برای دیباگ کردن مفید است.
        """
        return f"Drone('{self.id}', {self.position})"

    def move_to(self, new_position: tuple[int, int]):
        """
        پهپاد را به موقعیت جدیدی منتقل می‌کند و وضعیت آن را تغییر می‌دهد.
        (در حال حاضر یک جابجایی آنی است، در آینده می‌توانیم مصرف باتری و زمان را اضافه کنیم)
        """
        print(f"[{self.id}] Moving from {self.position} to {new_position}...")
        self.position = new_position
        self.status = "FLYING"
        # TODO: در آینده، مصرف باتری بر اساس مسافت طی شده محاسبه شود.
        # self.battery_level -= self.calculate_battery_consumption(distance)
        self.status = "IDLE" # پس از رسیدن، دوباره بیکار می‌شود.
        print(f"[{self.id}] Arrived at {new_position}. Status: {self.status}.")

    def report_status(self):
        """
        وضعیت فعلی پهپاد را چاپ می‌کند.
        """
        print(self.__str__())
