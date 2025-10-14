# =========================================================================
#  File: skymind_sim/layer_0_presentation/renderer.py
#  Author: Reza & AI Assistant | 2025-10-14 (Standardized Version)
#  Description: Manages all visual aspects of the simulation using Pygame.
# =========================================================================

import pygame
import logging
import os

class Renderer:
    """
    کلاس مسئول رندر کردن تمام اجزای شبیه‌سازی روی صفحه با استفاده از Pygame.
    این کلاس گرید، پهپادها و سایر اطلاعات را ترسیم می‌کند.
    """

    # تعریف رنگ‌ها به عنوان متغیرهای کلاس
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    COLOR_GRID_LINES = (200, 200, 200) # خاکستری روشن برای خطوط گرید
    COLOR_DRONE = (50, 50, 200)       # آبی برای پهپادها

    def __init__(self, config: dict):
        """
        سازنده کلاس رندرکننده.

        Args:
            config (dict): دیکشنری حاوی تنظیمات کامل برنامه.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing Pygame Renderer...")
        
        self.config = config
        
        try:
            # خواندن تنظیمات از کانفیگ
            self.screen_width = int(config['renderer']['screen_width'])
            self.screen_height = int(config['renderer']['screen_height'])
            self.cell_size = int(config['renderer']['cell_size'])
            self.fps = int(config['renderer']['fps'])
        except (KeyError, ValueError) as e:
            self.logger.error(f"Invalid renderer configuration: {e}")
            raise ValueError("Renderer configuration is missing or invalid.") from e

        # مقداردهی اولیه Pygame
        pygame.init()
        pygame.font.init()

        # ایجاد صفحه نمایش اصلی
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("SkyMind Simulator")

        self.drone_image = None
        self.font = None
        
        self.logger.info("Pygame Renderer initialized successfully.")

    def load_assets(self):
        """
        بارگذاری منابعی مانند تصاویر و فونت‌ها.
        این متد باید پس از مقداردهی اولیه Pygame فراخوانی شود.
        """
        self.logger.info("Loading assets...")
        try:
            # بارگذاری تصویر پهپاد
            drone_icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'images', 'drone_icon.png')
            raw_image = pygame.image.load(drone_icon_path).convert_alpha()
            # تغییر اندازه تصویر به اندازه سلول گرید
            self.drone_image = pygame.transform.scale(raw_image, (self.cell_size, self.cell_size))
            
            # بارگذاری فونت (اگر در کانفیگ مشخص شده باشد)
            font_path_str = self.config['renderer'].get('font_path')
            if font_path_str:
                font_path = os.path.join(os.path.dirname(__file__), '..', '..', font_path_str)
                font_size = int(self.config['renderer']['font_size'])
                self.font = pygame.font.Font(font_path, font_size)

            self.logger.info("Assets loaded successfully.")
        except Exception as e:
            self.logger.error(f"Failed to load assets: {e}")
            # در صورت عدم موفقیت، برنامه می‌تواند با اشکال پیش‌فرض ادامه دهد
            # بنابراین یک Exception ایجاد نمی‌کنیم، فقط لاگ می‌گیریم.

    def render(self, grid, entities):
        """
        رندر کردن یک فریم کامل از شبیه‌سازی.

        Args:
            grid (Grid): شیء گرید برای ترسیم.
            entities (list): لیستی از موجودیت‌ها (مانند پهپادها) برای ترسیم.
        """
        # 1. پاک کردن صفحه با رنگ پس‌زمینه سفید
        self.screen.fill(self.COLOR_WHITE)

        # 2. ترسیم گرید
        self._draw_grid(grid)

        # 3. ترسیم موجودیت‌ها (پهپادها)
        self._draw_entities(entities)

        # 4. به‌روزرسانی صفحه نمایش برای نمایش تغییرات
        pygame.display.flip()

    def _draw_grid(self, grid):
        """خطوط گرید را بر روی صفحه ترسیم می‌کند."""
        for x in range(0, grid.width * self.cell_size + 1, self.cell_size):
            pygame.draw.line(self.screen, self.COLOR_GRID_LINES, (x, 0), (x, grid.height * self.cell_size))
        for y in range(0, grid.height * self.cell_size + 1, self.cell_size):
            pygame.draw.line(self.screen, self.COLOR_GRID_LINES, (0, y), (grid.width * self.cell_size, y))

    def _draw_entities(self, entities):
        """موجودیت‌ها را بر اساس موقعیت آن‌ها در گرید ترسیم می‌کند."""
        for entity in entities:
            # تبدیل مختصات گرید به مختصات پیکسل روی صفحه
            pixel_x = entity.position[0] * self.cell_size
            pixel_y = entity.position[1] * self.cell_size
            
            if self.drone_image:
                # اگر تصویر پهپاد بارگذاری شده باشد، آن را ترسیم کن
                self.screen.blit(self.drone_image, (pixel_x, pixel_y))
            else:
                # در غیر این صورت، یک دایره آبی به جای آن ترسیم کن
                center_point = (pixel_x + self.cell_size // 2, pixel_y + self.cell_size // 2)
                pygame.draw.circle(self.screen, self.COLOR_DRONE, center_point, self.cell_size // 2)

