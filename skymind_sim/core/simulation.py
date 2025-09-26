# skymind_sim/core/simulation.py

import os
import time
import logging
from typing import TYPE_CHECKING

# این بلوک برای جلوگیری از خطاهای واردات چرخه‌ای (circular import) است.
if TYPE_CHECKING:
    from .environment import Environment

# لاگر را در سطح ماژول دریافت می‌کنیم. main.py آن را پیکربندی خواهد کرد.
logger = logging.getLogger("simulation_log")

class Simulation:
    """
    کلاس اصلی برای مدیریت و اجرای حلقه شبیه‌سازی.
    """
    def __init__(self, env: 'Environment', refresh_rate: float = 0.5):
        """
        سازنده کلاس شبیه‌سازی.

        :param env: شیء محیط شبیه‌سازی.
        :param refresh_rate: نرخ به‌روزرسانی نمایش در ثانیه (مثلاً 0.5 یعنی هر نیم ثانیه).
        """
        self.env = env
        self.refresh_rate = refresh_rate
        self.is_running = False
        self.step_count = 0

    def run(self):
        """
        حلقه اصلی شبیه‌سازی را اجرا می‌کند.
        """
        self.is_running = True
        logger.info("Simulation loop started.")
        
        try:
            while self.is_running:
                self._update()
                self._render()
                
                # بررسی شرط پایان شبیه‌سازی
                if not any(drone.is_active for drone in self.env.drones):
                    self.is_running = False
                    print("\nAll drones have completed their paths. Simulation finished.")
                    logger.info("All drones reached their destinations.")
                else:
                    time.sleep(self.refresh_rate)

        except KeyboardInterrupt:
            self.is_running = False
            print("\nSimulation interrupted by user (Ctrl+C).")
            logger.warning("Simulation interrupted by user.")
            
        except Exception as e:
            self.is_running = False
            logger.error(f"An error occurred during simulation run: {e}", exc_info=True)
            raise # خطا را مجدداً پرتاب می‌کنیم تا در main.py مدیریت شود

    def _update(self):
        """
        وضعیت تمام عناصر شبیه‌سازی را به‌روز می‌کند.
        """
        self.step_count += 1
        logger.debug(f"Simulation step: {self.step_count}")
        for drone in self.env.drones:
            if drone.is_active:
                drone.follow_path()
                logger.info(f"Drone '{drone.drone_id}' moved to {drone.position} at step {self.step_count}")

    def _render(self):
        """
        وضعیت فعلی شبیه‌سازی را در ترمینال نمایش می‌دهد.
        """
        # پاک کردن صفحه ترمینال (برای ویندوز 'cls' و برای لینوکس/مک 'clear')
        os.system('cls' if os.name == 'nt' else 'clear')

        print("--- SkyMind Real-time Simulation ---")
        print(f"Step: {self.step_count} | Active Drones: {sum(1 for d in self.env.drones if d.is_active)}")
        print("-" * 35)

        display_grid = self.env.get_display_grid()
        for row in display_grid:
            print(" ".join(row))
            
        print("-" * 35)
        print("Legend: S=Start, E=End, D=Drone, #=Obstacle")
