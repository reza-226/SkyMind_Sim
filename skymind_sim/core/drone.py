# skymind_sim/core/drone.py

from typing import Tuple, Optional

# تعریف نوع برای مختصات برای خوانایی بهتر
Position = Tuple[int, int]

class Drone:
    """
    نشان‌دهنده یک پهپاد در شبیه‌سازی.
    """
    def __init__(self, drone_id: str, start_position: Position, speed: int = 1, battery: float = 100.0):
        self.drone_id: str = drone_id
        self.position: Position = start_position
        self.speed: int = speed
        self.battery: float = battery
        self.status: str = 'IDLE'  # وضعیت‌های ممکن: IDLE, MOVING, RETURNING
        self.destination: Optional[Position] = None

    def __repr__(self) -> str:
        return (f"Drone(ID='{self.drone_id}', Position={self.position}, "
                f"Status='{self.status}', Battery={self.battery:.1f}%)")

    def report_status(self):
        """وضعیت فعلی پهپاد را با فرمت خوانا چاپ می‌کند."""
        print(
            f"[Drone {self.drone_id}] "
            f"Status: {self.status}, "
            f"Position: {self.position}, "
            f"Destination: {self.destination or 'None'}, "
            f"Battery: {self.battery:.1f}%"
        )

    def move_to(self, destination: Position):
        """
        برای پهپاد یک مقصد جدید تعیین کرده و وضعیت آن را به 'MOVING' تغییر می‌دهد.
        """
        if self.position == destination:
            print(f"[Drone {self.drone_id}] Already at destination {destination}.")
            return
            
        print(f"[Drone {self.drone_id}] Setting new destination: {destination}")
        self.destination = destination
        self.status = 'MOVING'

    def update(self):
        """
        منطق اصلی پهپاد در هر تیک شبیه‌سازی.
        اگر در حال حرکت باشد، یک قدم به سمت مقصد برمی‌دارد.
        """
        if self.status == 'MOVING' and self.destination:
            self._move_one_step()

   # در کلاس Drone، داخل فایل skymind_sim/core/drone.py

    def _move_one_step(self):
        """
        یک قدم به سمت مقصد حرکت می‌کند.
        منطق حرکت: ابتدا در محور X، سپس در محور Y.
        """
        if self.destination is None:
            return

        current_x, current_y = self.position
        dest_x, dest_y = self.destination
        
        # گام‌های بعدی در هر محور
        next_x, next_y = current_x, current_y

        # ابتدا حرکت در محور X
        if current_x != dest_x:
            # تعیین جهت حرکت در محور X
            step_x = 1 if dest_x > current_x else -1
            # حرکت به اندازه سرعت در آن جهت
            next_x += step_x * self.speed
            # اطمینان از اینکه از مقصد عبور نمی‌کنیم
            if (step_x > 0 and next_x > dest_x) or (step_x < 0 and next_x < dest_x):
                next_x = dest_x
        
        # اگر به مقصد X رسیدیم، حرکت در محور Y را شروع کن
        elif current_y != dest_y:
            # تعیین جهت حرکت در محور Y
            step_y = 1 if dest_y > current_y else -1
            # حرکت به اندازه سرعت در آن جهت
            next_y += step_y * self.speed
            # اطمینان از اینکه از مقصد عبور نمی‌کنیم
            if (step_y > 0 and next_y > dest_y) or (step_y < 0 and next_y < dest_y):
                next_y = dest_y

        # به‌روزرسانی موقعیت پهپاد
        self.position = (next_x, next_y)
        print(f"[Drone {self.drone_id}] Moved to {self.position}")
