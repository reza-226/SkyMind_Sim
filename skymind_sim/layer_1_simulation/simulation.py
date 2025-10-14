# =========================================================================
#  File: skymind_sim/layer_1_simulation/simulation.py
#  Author: Reza & AI Assistant | 2025-10-14 (Refactored Version)
# =========================================================================

import logging
import random

# وارد کردن کلاس‌های مورد نیاز از ماژول‌های دیگر
from ..layer_1_simulation.world.grid import Grid
from ..layer_1_simulation.scheduler import Scheduler
from ..layer_1_simulation.entities.drone import Drone


class Simulation:
    """
    موتور اصلی شبیه‌سازی که تمام اجزا را مدیریت می‌کند.
    این کلاس مسئولیت راه‌اندازی، اجرای گام به گام و نگهداری وضعیت کلی شبیه‌سازی را بر عهده دارد.
    """

    def __init__(self, config: dict):
        """
        سازنده کلاس شبیه‌سازی.

        Args:
            config (dict): دیکشنری حاوی تنظیمات کامل شبیه‌سازی.
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing the simulation engine...")

        # وضعیت شبیه‌سازی
        self.running = True
        self.steps = 0

        # --- ۱. راه‌اندازی اجزای اصلی ---
        
        # گرید (محیط)
        try:
            sim_config = self.config['simulation']
            grid_width = int(sim_config['width'])
            grid_height = int(sim_config['height'])
            cell_size = int(self.config['renderer']['cell_size'])
            
            self.grid = Grid(width=grid_width, height=grid_height, cell_size=cell_size)
        except (KeyError, ValueError) as e:
            self.logger.error(f"Failed to initialize grid due to invalid configuration: {e}")
            raise ValueError("Grid configuration is missing or invalid.") from e

        # زمان‌بند (Scheduler)
        self.scheduler = Scheduler()

        # --- ۲. راه‌اندازی موجودیت‌ها (Entities) ---
        self._setup_entities()

        self.logger.info("Simulation engine initialized successfully.")
        self.logger.info(f"Grid: {self.grid.width}x{self.grid.height}, Drones: {self.scheduler.get_agent_count()}")

    def _setup_entities(self):
        """پهپادها و سایر موجودیت‌ها را بر اساس کانفیگ مقداردهی اولیه می‌کند."""
        try:
            num_drones = int(self.config['simulation']['num_drones'])
        except (KeyError, ValueError):
            self.logger.warning("Could not find or parse 'num_drones' in config. Defaulting to 1 drone.")
            num_drones = 1
        
        self.logger.info(f"Setting up {num_drones} drone(s)...")

        for _ in range(num_drones):
            # انتخاب یک موقعیت شروع تصادفی و معتبر
            while True:
                start_x = random.randint(0, self.grid.width - 1)
                start_y = random.randint(0, self.grid.height - 1)
                # در آینده می‌توانیم بررسی کنیم که این سلول اشغال نشده باشد
                start_pos = (start_x, start_y)
                break  # فعلاً هر موقعیتی معتبر است

            # --- START: CHANGE HERE ---
            # پاس دادن دیکشنری config به سازنده Drone
            drone = Drone(config=self.config, position=start_pos, grid=self.grid)
            # --- END: CHANGE HERE ---

            # افزودن پهپاد به زمان‌بند تا در هر گام شبیه‌سازی، متد step آن فراخوانی شود.
            self.scheduler.add(drone)

    def step(self):
        """
        یک گام از شبیه‌سازی را اجرا می‌کند. این متد توسط حلقه اصلی برنامه فراخوانی می‌شود.
        """
        if not self.running:
            return
        
        # زمان‌بند، متد step() را برای تمام عوامل فعال (پهپادها) فراخوانی می‌کند.
        self.scheduler.step()
        self.steps += 1
        self.logger.debug(f"Simulation step {self.steps} completed.")

    def stop(self):
        """شبیه‌سازی را متوقف می‌کند."""
        self.running = False
        self.logger.info("Simulation stopped.")

    @property
    def entities(self):
        """لیستی از تمام موجودیت‌های فعال در شبیه‌سازی را برمی‌گرداند."""
        return self.scheduler.agents
