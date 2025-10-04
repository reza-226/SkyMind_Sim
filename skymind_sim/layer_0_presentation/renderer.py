# مسیر: skymind_sim/layer_0_presentation/renderer.py
import pygame
import logging
from skymind_sim.layer_0_presentation.asset_loader import load_image

class Renderer:
    """
    وظیفه: رندر محیط، مسیرها و پهپادها روی صفحه.
    """

    def __init__(self, environment):
        self.environment = environment
        self.window_config = self.environment.window_config
        self.grid_config = self.environment.grid_config

        self.cell_size = self.grid_config.get("cell_size", 32)
        width_px = self.grid_config.get("width", 20) * self.cell_size
        height_px = self.grid_config.get("height", 20) * self.cell_size

        pygame.init()
        self.screen = pygame.display.set_mode((width_px, height_px))
        pygame.display.set_caption(self.window_config.get("title", "SkyMind Simulation"))

        self.drone_image = load_image("drone.png", scale=self.cell_size)
        self.background_color = (255, 255, 255)
        self.obstacle_color = (100, 100, 100)
        self.path_color = (0, 255, 0)

    def draw_grid(self):
        for x in range(0, self.screen.get_width(), self.cell_size):
            pygame.draw.line(self.screen, (200, 200, 200), (x, 0), (x, self.screen.get_height()))
        for y in range(0, self.screen.get_height(), self.cell_size):
            pygame.draw.line(self.screen, (200, 200, 200), (0, y), (self.screen.get_width(), y))

    def draw_obstacles(self):
        for (ox, oy, ow, oh) in self.environment.get_obstacles_data():
            rect = pygame.Rect(ox, oy, ow, oh)
            pygame.draw.rect(self.screen, self.obstacle_color, rect)

    def draw_paths(self):
        """
        رسم مسیرهای ذخیره شده در environment و (در آینده) مسیرهای دیگر پهپادها.
        """
        paths = self.environment.get_path_to_draw()
        if not paths:
            return
        for path in paths:
            for (px, py) in path:
                rect = pygame.Rect(px, py, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.path_color, rect, 2)

    def draw_test_drone(self):
        """
        رسم تصویر پهپاد تستی در موقعیت فعلی.
        """
        if hasattr(self.environment, "test_drone_pos") and self.environment.test_drone_pos is not None:
            x_cell, y_cell = self.environment.test_drone_pos
            self.screen.blit(self.drone_image, (x_cell * self.cell_size, y_cell * self.cell_size))

    def draw_path_overlay(self):
        """
        رسم یک لایه‌ی نیمه‌شفاف برای نمایش مسیر فعلی پهپاد (S=سبز، G=قرمز، *=آبی).
        """
        if not hasattr(self.environment, "test_drone_path") or not self.environment.test_drone_path:
            return

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        path = self.environment.test_drone_path
        start = path[0]
        goal = path[-1]

        # مسیر → آبی نیمه‌شفاف
        for px, py in path:
            pygame.draw.rect(overlay, (0, 0, 255, 80),
                             (px * self.cell_size, py * self.cell_size, self.cell_size, self.cell_size))

        # نقطه شروع → سبز نیمه‌شفاف
        pygame.draw.rect(overlay, (0, 255, 0, 120),
                         (start[0] * self.cell_size, start[1] * self.cell_size, self.cell_size, self.cell_size))

        # نقطه هدف → قرمز نیمه‌شفاف
        pygame.draw.rect(overlay, (255, 0, 0, 120),
                         (goal[0] * self.cell_size, goal[1] * self.cell_size, self.cell_size, self.cell_size))

        self.screen.blit(overlay, (0, 0))

    def render_frame(self):
        """
        رندر کامل یک فریم از شبیه سازی.
        """
        self.screen.fill(self.background_color)
        self.draw_grid()
        self.draw_obstacles()
        self.draw_paths()
        self.draw_test_drone()
        self.draw_path_overlay()  # اضافه شدن مسیر گرافیکی به فریم
        pygame.display.flip()
