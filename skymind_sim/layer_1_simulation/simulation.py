import pygame
import logging
from skymind_sim.layer_0_presentation.environment import Environment
from skymind_sim.layer_1_simulation.entities.drone import Drone

class Simulation:
    """
    کلاس اصلی مدیریت شبیه‌سازی.
    این کلاس مسئول ایجاد محیط، پهپادها و اجرای حلقه اصلی شبیه‌سازی است.
    """
    def __init__(self, config: dict):
        """
        سازنده کلاس Simulation.

        Args:
            config (dict): دیکشنری حاوی تمام تنظیمات شبیه‌سازی.
        """
        self.config = config
        self.running = False
        
        # مقداردهی اولیه Pygame
        try:
            pygame.init()
            logging.info("Pygame با موفقیت مقداردهی اولیه شد.")
        except pygame.error as e:
            logging.critical(f"خطا در مقداردهی اولیه Pygame: {e}")
            raise

        # ایجاد محیط (شامل پنجره و موانع)
        self.environment = Environment(config=self.config)
        
        # ایجاد پهپادها
        self.drones = self._create_drones()

    def _create_drones(self) -> list:
        """
        لیستی از اشیاء پهپاد را بر اساس تنظیمات کانفیگ ایجاد می‌کند.
        """
        drones_list = []
        drones_config = self.config.get("drones", [])
        if not drones_config:
            logging.warning("هیچ پهپادی در فایل کانفیگ تعریف نشده است.")
            return drones_list
            
        for drone_conf in drones_config:
            try:
                drone = Drone(config=drone_conf)
                drones_list.append(drone)
            except Exception as e:
                logging.error(f"خطا در ایجاد پهپاد با کانفیگ {drone_conf}: {e}")
        return drones_list

    def run(self):
        """
        حلقه اصلی شبیه‌سازی را اجرا می‌کند.
        """
        logging.info("شبیه‌سازی شروع شد.")
        self.running = True
        clock = pygame.time.Clock()
        time_step = self.config.get("simulation", {}).get("time_step", 1.0 / 60.0)

        while self.running:
            # 1. مدیریت رویدادها (Event Handling)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # سایر رویدادها مانند ورودی کیبورد در اینجا مدیریت می‌شوند

            # 2. به‌روزرسانی وضعیت (Update State)
            self._update(time_step)

            # 3. رندر کردن (Render)
            self._render()

            # تنظیم نرخ فریم
            clock.tick(self.config.get("window", {}).get("fps", 60))

        logging.info("حلقه شبیه‌سازی پایان یافت. در حال خروج...")
        pygame.quit()

    def _update(self, dt: float):
        """
        وضعیت تمام اشیاء داخل شبیه‌سازی را به‌روزرسانی می‌کند.
        """
        for drone in self.drones:
            drone.update(dt)

    def _render(self):
        """
        تمام اشیاء را روی صفحه رسم می‌کند.
        """
        self.environment.draw_background()
        self.environment.draw_obstacles()
        
        for drone in self.drones:
            self.environment.draw_drone(drone)
            
        pygame.display.flip()
