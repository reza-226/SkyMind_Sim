import pygame
import logging
import json

class Environment:
    """
    کلاس مدیریت محیط، شامل پنجره، پس‌زمینه و بارگذاری نقشه.
    """
    def __init__(self, config: dict):
        """
        سازنده کلاس Environment.

        Args:
            config (dict): دیکشنری کامل تنظیمات برنامه.
        """
        window_settings = config.get("window", {})
        env_settings = config.get("environment", {})
        sim_settings = config.get("simulation", {})
        
        self.width = window_settings.get("width", 800)
        self.height = window_settings.get("height", 600)
        caption = window_settings.get("caption", "Simulation")
        
        self.background_color = env_settings.get("background_color", (255, 255, 255))
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(caption)
        
        self.obstacles = []
        self.map_filepath = sim_settings.get("map_path")
        if self.map_filepath:
            self._load_map(self.map_filepath)
        else:
            logging.warning("هیچ مسیری برای فایل نقشه ('map_path') در کانفیگ مشخص نشده است. محیط بدون مانع خواهد بود.")

    def _load_map(self, filepath: str):
        """موانع را از یک فایل نقشه JSON بارگذاری می‌کند."""
        try:
            with open(filepath, 'r') as f:
                map_data = json.load(f)
            
            # هر مانع به صورت [x, y, width, height] تعریف شده است
            for obs_data in map_data.get("obstacles", []):
                rect = pygame.Rect(obs_data[0], obs_data[1], obs_data[2], obs_data[3])
                self.obstacles.append(rect)
            
            logging.info(f"{len(self.obstacles)} مانع با موفقیت از '{filepath}' بارگذاری شد.")
        except FileNotFoundError:
            logging.error(f"فایل نقشه در مسیر '{filepath}' یافت نشد.")
        except json.JSONDecodeError:
            logging.error(f"خطا در پارس کردن فایل JSON نقشه: '{filepath}'")
        except Exception as e:
            logging.error(f"خطای پیش‌بینی نشده در بارگذاری نقشه: {e}")

    def draw_background(self):
        """پس‌زمینه صفحه را رسم می‌کند."""
        self.screen.fill(self.background_color)

    def draw_obstacles(self):
        """تمام موانع را روی صفحه رسم می‌کند."""
        obstacle_color = (100, 100, 100) # رنگ خاکستری برای موانع
        for obs in self.obstacles:
            pygame.draw.rect(self.screen, obstacle_color, obs)

    def draw_drone(self, drone):
        """یک پهپاد را روی صفحه رسم می‌کند."""
        # اگر پهپاد تصویر دارد، تصویر را رسم کن
        if drone.asset:
            # مرکز تصویر را با موقعیت پهپاد هماهنگ کن
            pos_x, pos_y = drone.position
            asset_rect = drone.asset.get_rect(center=(int(pos_x), int(pos_y)))
            self.screen.blit(drone.asset, asset_rect)
        # در غیر این صورت، یک دایره ساده رسم کن
        else:
            pygame.draw.circle(self.screen, drone.color, (int(drone.position[0]), int(drone.position[1])), 10)
