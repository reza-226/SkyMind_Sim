# skymind_sim/layer_1_simulation/world/obstacle.py

import pygame

class Obstacle:
    """
    نشان‌دهنده یک مانع ثابت در محیط شبیه‌سازی.
    این کلاس اطلاعات مربوط به موقعیت، اندازه و رنگ مانع را نگهداری می‌کند
    و همچنین نحوه ترسیم آن روی صفحه را مدیریت می‌کند.
    """
    def __init__(self, rect: pygame.Rect, color: tuple = (100, 100, 100)):
        """
        سازنده کلاس Obstacle.

        Args:
            rect (pygame.Rect): یک شیء Rect از Pygame که موقعیت (x, y) و 
                                اندازه (width, height) مانع را مشخص می‌کند.
            color (tuple, optional): رنگ مانع به صورت (R, G, B). 
                                     پیش‌فرض (100, 100, 100) است.
        """
        self.rect = rect
        self.color = color

    def render(self, surface: pygame.Surface):
        """
        مانع را به صورت یک مستطیل روی سطح (surface) داده شده ترسیم می‌کند.

        Args:
            surface (pygame.Surface): سطحی که مانع باید روی آن کشیده شود 
                                      (معمولاً صفحه اصلی بازی).
        """
        pygame.draw.rect(surface, self.color, self.rect)
