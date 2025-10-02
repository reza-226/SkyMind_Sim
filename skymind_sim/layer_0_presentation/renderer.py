# skymind_sim/layer_0_presentation/renderer.py
import pygame
from typing import Dict, Any

# وارد کردن AssetLoader از مسیر جدیدش در لایه ۰
from skymind_sim.layer_0_presentation.asset_loader import asset_loader

# تعریف رنگ‌ها
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OBSTACLE_COLOR = (100, 100, 100)
TEXT_COLOR = (230, 230, 230)

class Renderer:
    def __init__(self, width: int, height: int):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("SkyMind_Sim")
        
        # بارگذاری فونت و تصویر با استفاده از AssetLoader
        # فرض بر این است که فایل فونت Vazirmatn-Regular.ttf در پوشه assets/fonts وجود دارد
        self.font_small = asset_loader.load_font("Vazirmatn-Regular.ttf", 18)
        
        # فرض بر این است که فایل drone.png در پوشه assets/images وجود دارد
        drone_image_original = asset_loader.load_image("drone.png")
        self.drone_image = pygame.transform.scale(drone_image_original, (40, 40))
        
        print("Renderer (Layer 0) initialized.")

    def draw(self, world_state: Dict[str, Any]):
        """وضعیت دنیا را روی صفحه رسم می‌کند."""
        self.screen.fill(BLACK)
        
        # رسم موانع
        for obstacle in world_state.get('obstacles', []):
            rect = pygame.Rect(obstacle['position'][0], obstacle['position'][1], obstacle['size'][0], obstacle['size'][1])
            pygame.draw.rect(self.screen, OBSTACLE_COLOR, rect)
            
        # رسم پهپادها
        for drone in world_state.get('drones', []):
            pos = drone['position']
            # مرکز تصویر پهپاد را روی موقعیت آن تنظیم می‌کنیم
            top_left = (pos[0] - self.drone_image.get_width() / 2, pos[1] - self.drone_image.get_height() / 2)
            self.screen.blit(self.drone_image, top_left)
            
        # نمایش زمان شبیه‌سازی
        sim_time = world_state.get('time', 0.0)
        time_text = self.font_small.render(f"Time: {sim_time:.2f}s", True, TEXT_COLOR)
        self.screen.blit(time_text, (10, 10))
        
        # به‌روزرسانی صفحه نمایش
        pygame.display.flip()

    def handle_events(self) -> bool:
        """رویدادهای پنجره را مدیریت می‌کند (مثلاً بستن پنجره)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # سیگنال برای خروج از حلقه اصلی
        return True

    def cleanup(self):
        """منابع Pygame را آزاد می‌کند."""
        print("Cleaning up Renderer resources.")
        pygame.quit()
