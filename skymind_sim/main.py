# FILE: skymind_sim/main.py

import pygame

# وارد کردن مستقیم کلاس‌ها از فایل‌هایشان
from skymind_sim.core.environment import Environment
from skymind_sim.core.simulation import Simulation 
from skymind_sim.utils.asset_loader import get_asset_loader

# --- ثابت‌ها ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def main():
    """تابع اصلی برای مقداردهی اولیه و اجرای شبیه‌سازی."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("SkyMind Drone Simulator")

    # AssetLoader را بعد از راه‌اندازی pygame مقداردهی اولیه کنید
    asset_loader = get_asset_loader()
    asset_loader.initialize() # این متد را برای بارگذاری منابع فراخوانی می‌کنیم
    
    env = Environment(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    env.create_drones(5) 

    sim = Simulation(
        environment=env,
        screen=screen,
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT
    )

    sim.run()
    pygame.quit()

if __name__ == '__main__':
    main()
