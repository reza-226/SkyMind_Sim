# FILE: skymind_sim/core/simulation.py

import pygame
# وارد کردن مستقیم از فایل
from skymind_sim.utils.asset_loader import get_asset_loader

class Simulation:
    def __init__(self, environment, screen, width, height, fps=60):
        self.environment = environment
        self.screen = screen
        self.width = width
        self.height = height
        self.fps = fps
        self.running = True
        self.clock = pygame.time.Clock()
        
        self.asset_loader = get_asset_loader()
        
        # دسترسی مستقیم به منابع بارگذاری شده
        self.drone_icon = self.asset_loader.images.get('drone_default')
        self.font = self.asset_loader.fonts.get('technical_small')

        if not self.font or not self.drone_icon:
            raise RuntimeError("CRITICAL: Font or Drone Icon not loaded properly. Check AssetLoader logs.")

    def run(self):
        """حلقه اصلی شبیه‌سازی."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

    def handle_events(self):
        """پردازش ورودی کاربر."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """به‌روزرسانی وضعیت شبیه‌سازی."""
        self.environment.update_all()

    def render(self):
        """رسم همه چیز روی صفحه."""
        self.screen.fill((50, 50, 50))
        self._draw_drones()
        pygame.display.flip()

    def _draw_drones(self):
        """رسم تمام پهپادها."""
        for drone in self.environment.get_all_drones():
            angle = drone.get_bearing_degrees()
            rotated_icon = pygame.transform.rotate(self.drone_icon, angle)
            new_rect = rotated_icon.get_rect(center=drone.position)
            self.screen.blit(rotated_icon, new_rect.topleft)
            
            text_surface = self.font.render(drone.name, True, (255, 255, 255))
            text_y_offset = self.drone_icon.get_height() / 2 + 5
            text_rect = text_surface.get_rect(center=(drone.position[0], drone.position[1] + text_y_offset))
            self.screen.blit(text_surface, text_rect)
