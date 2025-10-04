import logging
import time

class Scheduler:
    def __init__(self, environment, simulation_config):
        self.environment = environment
        self.simulation_config = simulation_config

        # گرفتن logger
        self.logger = logging.getLogger("SkyMind")

        # مقداردهی اولیه شمارنده‌ها
        self.time_step = float(self.simulation_config.get("time_step", 0.1))
        self.max_time = self.simulation_config.get("max_time", None)
        self.max_ticks = self.simulation_config.get("max_ticks", None)

        self.current_time = 0.0
        self.tick_count = 0
        self._finished = False

        self.logger.info(
            f"[Scheduler] Started with time_step={self.time_step}, "
            f"max_time={self.max_time}, max_ticks={self.max_ticks}"
        )

    def update(self):
        """یک قدم شبیه‌سازی رو اجرا می‌کنه"""
        if self._finished:
            return

        # انجام آپدیت محیط
        self.environment.update(self.time_step)

        # به‌روزرسانی زمان و شمارنده تیک‌ها
        self.current_time += self.time_step
        self.tick_count += 1

        # چک کردن پایان
        if self.is_finished():
            self.logger.info(
                f"[Scheduler] Finished at time={self.current_time:.2f}s, "
                f"ticks={self.tick_count}"
            )
            self._finished = True

    def is_finished(self):
        """بررسی می‌کنه که آیا شبیه‌سازی باید متوقف بشه یا نه"""
        if self.max_time is not None and self.current_time >= self.max_time:
            return True
        if self.max_ticks is not None and self.tick_count >= self.max_ticks:
            return True
        return False

    def stop(self):
        """توقف دستی شبیه‌سازی"""
        self._finished = True
        self.logger.warning("[Scheduler] Simulation stopped manually.")
