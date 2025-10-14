# =========================================================================
#  File: skymind_sim/layer_1_simulation/entities/drone.py
#  Author: Reza & AI Assistant | 2025-10-14 (Refactored Version)
# =========================================================================
import logging

class Drone:
    """
    نشان‌دهنده یک پهپاد در شبیه‌سازی. این یک عامل فعال است.
    """
    _id_counter = 0

    def __init__(self, position: tuple[int, int], grid):
        """
        سازنده کلاس پهپاد.

        Args:
            position (tuple[int, int]): موقعیت اولیه (x, y) پهپاد روی گرید.
            grid: ارجاعی به شیء گرید برای آگاهی از محیط.
        """
        Drone._id_counter += 1
        self.id = Drone._id_counter
        self.position = position
        self.grid = grid  # پهپاد از محیط خود آگاه است
        self.logger = logging.getLogger(f"{__name__}.Drone_{self.id}")
        
        self.logger.info(f"Drone {self.id} created at position {self.position}.")

    def step(self):
        """
        یک گام از منطق پهپاد را اجرا می‌کند.
        این متد توسط Scheduler در هر تیک شبیه‌سازی فراخوانی می‌شود.
        """
        # در آینده: منطق حرکت، تصمیم‌گیری، مصرف باتری و ... اینجا قرار می‌گیرد.
        self.logger.debug(f"Drone {self.id} is performing its step action at {self.position}.")
        # مثال: حرکت تصادفی ساده (فعلا غیرفعال)
        # self.move_randomly()

    def move_randomly(self):
        """یک مثال از حرکت تصادفی."""
        import random
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy

        # بررسی مرزهای گرید
        if 0 <= new_x < self.grid.width and 0 <= new_y < self.grid.height:
            self.position = (new_x, new_y)
            self.logger.info(f"Drone {self.id} moved to {self.position}.")

    def __repr__(self):
        return f"Drone(id={self.id}, position={self.position})"
