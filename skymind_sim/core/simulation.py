# skymind_sim/core/simulation.py

import time
from .environment import Environment

class Simulation:
    """
    موتور اصلی شبیه‌سازی. این کلاس حلقه اصلی، مدیریت زمان و به‌روزرسانی
    وضعیت تمام موجودیت‌های داخل محیط را بر عهده دارد.
    """
    def __init__(self, environment: Environment):
        """
        سازنده کلاس شبیه‌سازی.

        Args:
            environment (Environment): محیطی که شبیه‌سازی در آن اجرا می‌شود.
        """
        self.environment: Environment = environment
        self.current_tick: int = 0
        self.is_running: bool = False

    def run(self, max_ticks: int = 100, tick_duration: float = 0.1):
        """
        حلقه اصلی شبیه‌سازی را اجرا می‌کند.

        Args:
            max_ticks (int): حداکثر تعداد تیک‌هایی که شبیه‌سازی اجرا می‌شود.
            tick_duration (float): مدت زمان واقعی هر تیک به ثانیه (برای کنترل سرعت نمایش).
        """
        print("\n=========================================")
        print("    ▶️  Starting Simulation Run ▶️")
        print("=========================================")
        self.is_running = True
        
        for tick in range(max_ticks):
            if not self.is_running:
                print("Simulation stopped manually.")
                break
                
            self.current_tick = tick
            print(f"\n--- Tick: {self.current_tick} ---")
            
            # 1. به‌روزرسانی تمام موجودیت‌ها در محیط
            self.update_entities()
            
            # 2. نمایش وضعیت فعلی محیط
            self.environment.display()
            
            # 3. بررسی شرایط پایان
            if self.check_termination_conditions():
                print("Termination condition met. Ending simulation.")
                self.is_running = False
                break
            
            # مکث کوتاه برای کنترل سرعت شبیه‌سازی
            time.sleep(tick_duration)
            
        print("\n=========================================")
        print("    ⏹️  Simulation Run Finished ⏹️")
        print(f"    Total Ticks: {self.current_tick + 1}")
        print("=========================================")


        # در فایل skymind_sim/core/simulation.py

    def update_entities(self):
        """
        وضعیت تمام موجودیت‌ها را برای تیک فعلی به‌روز می‌کند.
        """
        print("[Simulation] Updating all entities...")
        for drone in self.environment.drones:
            # فراخوانی متد update خود پهپاد
            drone.update()
            
            # همگام‌سازی موقعیت پهپاد با نقشه محیط
            self.environment.update_drone_position(drone)


    def check_termination_conditions(self) -> bool:
        """
        بررسی می‌کند که آیا شبیه‌سازی باید پایان یابد یا خیر.
        (فعلاً همیشه False برمی‌گرداند تا به max_ticks برسد)
        """
        # مثال برای آینده: اگر همه پهپادها به مقصد رسیدند
        # all_idle = all(d.status == 'IDLE' for d in self.environment.drones)
        # if all_idle and self.current_tick > 0:
        #     return True
        return False

    def stop(self):
        """ شبیه‌سازی را متوقف می‌کند. """
        self.is_running = False
