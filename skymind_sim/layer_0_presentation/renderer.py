# skymind_sim/layer_0_presentation/renderer.py

import pygame
from typing import List

# از آنجایی که این فایل‌ها در لایه‌های مختلف هستند، از import نسبی استفاده می‌کنیم
# این import ها برای Type Hinting لازم هستند تا کد خواناتر باشد
from ..layer_1_simulation.entities.drone import Drone
from .environment import Environment


class Renderer:
    """
    این کلاس مسئولیت ترسیم تمام اجزای شبیه‌سازی روی صفحه را بر عهده دارد.
    این کلاس مستقیماً اشیاء شبیه‌سازی (مانند Environment و Drone) را برای ترسیم دریافت می‌کند.
    """
    def __init__(self, screen: pygame.Surface, config: dict):
        """
        سازنده کلاس Renderer.

        Args:
            screen (pygame.Surface): سطحی که ترسیم روی آن انجام می‌شود (پنجره اصلی).
            config (dict): دیکشنری کلی تنظیمات برای دسترسی به رنگ‌ها، فونت‌ها و غیره.
        """
        self.screen = screen
        self.config = config
        
        # استخراج تنظیمات رندر از کانفیگ کلی
        render_settings = self.config.get("render_settings", {})
        
        # تعریف رنگ‌ها از کانفیگ
        self.colors = render_settings.get("colors", {
            "background": (240, 240, 240),
            "obstacle": (50, 50, 50),
            "drone": (200, 50, 50),
            "grid": (220, 220, 220),
            "path": (0, 150, 255),
            "text": (10, 10, 10)
        })

        # TODO: بارگذاری فونت و تصاویر پهپاد در آینده از طریق AssetLoader انجام شود
        self.font = pygame.font.SysFont(None, 24) # استفاده از فونت پیش‌فرض برای سادگی
        self.drone_img = None  # فعلا از تصویر استفاده نمی‌کنیم و دایره رسم می‌کنیم

    def draw(self, environment: Environment, drones: List[Drone]):
        """
        یک فریم کامل از شبیه‌سازی را ترسیم می‌کند.
        این متد جایگزین متد render قبلی است و اشیاء را مستقیماً دریافت می‌کند.
        
        Args:
            environment (Environment): آبجکت محیط شامل موانع و ابعاد.
            drones (List[Drone]): لیستی از آبجکت‌های پهپاد برای ترسیم.
        """
        # 1. ترسیم پس‌زمینه
        self.screen.fill(self.colors.get("background", (255, 255, 255)))

        # 2. ترسیم گرید (اختیاری)
        # self._draw_grid(environment.grid_size) # در صورت نیاز می‌توانید فعال کنید

        # 3. ترسیم موانع از آبجکت environment
        self._draw_obstacles(environment.obstacles)

        # 4. ترسیم پهپادها
        if drones:
            self._draw_drones(drones)
        
        # نیازی به pygame.display.flip() در اینجا نیست، این کار در حلقه اصلی انجام می‌شود.

    def _draw_grid(self, grid_size: int):
        """یک گرید پس‌زمینه برای راهنمایی بصری ترسیم می‌کند."""
        width = self.screen.get_width()
        height = self.screen.get_height()
        grid_color = self.colors.get("grid", (230, 230, 230))
        for x in range(0, width, grid_size):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, height))
        for y in range(0, height, grid_size):
            pygame.draw.line(self.screen, grid_color, (0, y), (width, y))

    def _draw_obstacles(self, obstacles: list):
        """موانع را ترسیم می‌کند."""
        obstacle_color = self.colors.get("obstacle", (50, 50, 50))
        for obstacle in obstacles:
            pygame.draw.rect(self.screen, obstacle_color, obstacle.rect)

    def _draw_drone_path(self, drone: Drone):
        """مسیر برنامه‌ریزی شده برای یک پهپاد را ترسیم می‌کند."""
        path_color = self.colors.get("path", (0, 150, 255))
        # TODO: مسیر پهپاد باید از آبجکت drone خوانده شود. فعلا این بخش غیرفعال است.
        # if drone.path and len(drone.path) > 1:
        #     pygame.draw.lines(self.screen, path_color, False, drone.path, 3)
        pass # موقتاً غیرفعال

    def _draw_drones(self, drones: List[Drone]):
        """پهپادها را ترسیم می‌کند."""
        drone_color = self.colors.get("drone", (200, 50, 50))
        text_color = self.colors.get("text", (10, 10, 10))

        for drone in drones:
            self._draw_drone_path(drone)
            
            if self.drone_img:
                img_rect = self.drone_img.get_rect(center=drone.position)
                self.screen.blit(self.drone_img, img_rect)
            else:
                # ترسیم یک دایره به جای تصویر پهپاد
                pygame.draw.circle(self.screen, drone_color, (int(drone.position[0]), int(drone.position[1])), 15)

            # نمایش ID پهپاد
            id_text = self.font.render(str(drone.drone_id), True, text_color)
            text_rect = id_text.get_rect(center=(drone.position[0], drone.position[1] - 25))
            self.screen.blit(id_text, text_rect)
