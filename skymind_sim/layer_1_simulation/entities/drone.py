# =========================================================================
#  File: skymind_sim/layer_1_simulation/entities/drone.py
#  Author: Reza & AI Assistant | 2025-10-14 (Updated for Movement)
#  Description: Defines the Drone entity in the simulation.
# =========================================================================

import logging
import random # <--- ایمپورت کردن کتابخانه random

class Drone:
    """
    نشان‌دهنده یک پهپاد در شبیه‌سازی. این کلاس ویژگی‌ها و رفتارهای
    پهپاد مانند موقعیت، حرکت و وضعیت باتری را مدیریت می‌کند.
    """
    _id_counter = 0

    @classmethod
    def _generate_id(cls):
        """یک شناسه منحصر به فرد برای هر پهپاد جدید تولید می‌کند."""
        cls._id_counter += 1
        return cls._id_counter
    
    @classmethod
    def reset_id_counter(cls):
        """شمارنده شناسه را برای تست‌ها یا اجرای مجدد شبیه‌سازی ریست می‌کند."""
        cls._id_counter = 0

    def __init__(self, config: dict, grid, position: tuple[int, int]):
        """
        سازنده کلاس پهپاد.

        Args:
            config (dict): دیکشنری تنظیمات.
            grid (Grid): شیء گرید که پهپاد در آن قرار دارد.
            position (tuple[int, int]): موقعیت اولیه (x, y) پهپاد.
        """
        self.id = self._generate_id()
        self.config = config
        self.grid = grid
        self.position = position
        
        # نام لاگر را بر اساس شناسه پهپاد تنظیم می‌کنیم تا لاگ‌ها قابل تفکیک باشند
        self.logger = logging.getLogger(f"{__name__}.Drone_{self.id}")
        self.logger.info(f"Drone {self.id} created at position {self.position}.")

    def step(self):
        """
        یک گام از منطق پهپاد را اجرا می‌کند.
        در این پیاده‌سازی اولیه، پهپاد به صورت تصادفی حرکت می‌کند.
        """
        # انتخاب یک جهت تصادفی: (dx, dy)
        # (0, 1): پایین, (0, -1): بالا, (1, 0): راست, (-1, 0): چپ
        move_x, move_y = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        
        # محاسبه موقعیت جدید
        new_x = self.position[0] + move_x
        new_y = self.position[1] + move_y

        # بررسی اینکه آیا موقعیت جدید داخل مرزهای گرید است
        if 0 <= new_x < self.grid.width and 0 <= new_y < self.grid.height:
            # اگر معتبر بود، موقعیت را به‌روز کن
            self.position = (new_x, new_y)
            # این لاگ برای دیباگ کردن حرکت بسیار مفید است
            self.logger.debug(f"Drone {self.id} moved to {self.position}")
        else:
            # اگر حرکت خارج از مرز بود، در جای خود باقی بمان
            self.logger.debug(f"Drone {self.id} attempted to move out of bounds to ({new_x}, {new_y}). Staying at {self.position}.")

    def __repr__(self):
        """بازنمایی رشته‌ای شیء پهپاد برای نمایش بهتر در لاگ‌ها و دیباگ."""
        return f"Drone(id={self.id}, position={self.position})"
