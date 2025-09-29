# skymind_sim/core/simulation.py

from skymind_sim.core.environment import Environment

class Simulation:
    """
    موتور اصلی شبیه‌سازی که وضعیت محیط را در طول زمان مدیریت می‌کند.
    """
    def __init__(self, environment: Environment, total_time: int, time_step: float = 1.0):
        """
        سازنده کلاس Simulation.

        Args:
            environment (Environment): شیء محیط که شبیه‌سازی در آن اجرا می‌شود.
            total_time (int): کل زمان شبیه‌سازی بر حسب ثانیه.
            time_step (float): گام زمانی برای هر مرحله از شبیه‌سازی (بر حسب ثانیه).
        """
        if not isinstance(environment, Environment):
            raise TypeError("ورودی 'environment' باید یک نمونه از کلاس Environment باشد.")
        if not isinstance(total_time, (int, float)) or total_time <= 0:
            raise ValueError("total_time باید یک عدد مثبت باشد.")
        if not isinstance(time_step, (int, float)) or time_step <= 0:
            raise ValueError("time_step باید یک عدد مثبت باشد.")

        self._environment = environment
        self._total_time = total_time
        self._time_step = time_step
        self._current_time = 0.0

    @property
    def environment(self) -> Environment:
        return self._environment

    @property
    def total_time(self) -> int:
        return self._total_time

    @property
    def time_step(self) -> float:
        return self._time_step

    @property
    def current_time(self) -> float:
        return self._current_time

    def run_step(self):
        """
        یک گام از شبیه‌سازی را اجرا می‌کند.
        """
        if self._current_time >= self._total_time:
            # print("پایان شبیه‌سازی.")
            return

        # حرکت دادن تمام پهپادها
        for drone in self.environment.drones:
            drone.move(self._time_step)
        
        # افزایش زمان
        self._current_time += self._time_step

    def get_current_positions(self) -> dict:
        """
        موقعیت فعلی تمام پهپادها را برمی‌گرداند.

        Returns:
            dict: دیکشنری که کلید آن شناسه پهپاد و مقدار آن موقعیت فعلی است.
        """
        return {drone.drone_id: drone.position for drone in self.environment.drones}
    
    def __repr__(self) -> str:
        return f"Simulation(time={self.current_time:.2f}/{self.total_time}, step={self.time_step})"
