import pygame
import numpy as np
import logging

class Drone:
    """
    این کلاس نمایانگر یک پهپاد در شبیه‌سازی است.
    """
    def __init__(self, config: dict):
        """
        سازنده کلاس Drone.

        Args:
            config (dict): دیکشنری تنظیمات مربوط به این پهپاد خاص.
        """
        try:
            self.id = config["id"]
            self.position = np.array(config["position"], dtype=float)
            self.destination = np.array(config["destination"], dtype=float)
            self.speed = config["speed"]
            self.color = config.get("color", (0, 0, 255))
            
            # بارگذاری تصویر پهپاد
            self.asset_path = config.get("asset_path")
            self.asset = None
            if self.asset_path:
                try:
                    self.asset = pygame.image.load(self.asset_path).convert_alpha()
                    # می‌توانید اندازه تصویر را در اینجا تغییر دهید
                    # self.asset = pygame.transform.scale(self.asset, (30, 30))
                except pygame.error as e:
                    logging.error(f"خطا در بارگذاری تصویر پهپاد از مسیر '{self.asset_path}': {e}")
                    self.asset = None

            logging.info(f"پهپاد {self.id} در موقعیت {self.position.tolist()} با مقصد اولیه {self.destination.tolist()} ایجاد شد.")

        except KeyError as e:
            logging.error(f"خطا در خواندن اطلاعات پهپاد از کانفیگ. کلید '{e.args[0]}' یافت نشد.")
            raise

    def update(self, dt: float):
        """
        موقعیت پهپاد را بر اساس سرعت و مقصدش به‌روزرسانی می‌کند.

        Args:
            dt (float): زمان سپری شده از آخرین فریم (delta time).
        """
        direction = self.destination - self.position
        distance = np.linalg.norm(direction)

        # اگر پهپاد به مقصد نرسیده باشد، حرکت کن
        if distance > 1.0:  # یک آستانه کوچک برای جلوگیری از لرزش در مقصد
            # نرمال‌سازی بردار جهت
            direction_normalized = direction / distance
            # محاسبه جابجایی در این فریم
            displacement = direction_normalized * self.speed * dt
            
            # اگر جابجایی بیشتر از فاصله تا مقصد باشد، پهپاد را مستقیم به مقصد ببر
            if np.linalg.norm(displacement) > distance:
                self.position = self.destination
            else:
                self.position += displacement
