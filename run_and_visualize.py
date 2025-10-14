# =========================================================================
#  File: run_and_visualize.py
#  Author: Reza & AI Assistant | 2025-10-14 (Finalized Version)
#  Description: Entry point for running and visualizing the SkyMind simulation.
# =========================================================================

import logging
import sys
import os
import pygame

# افزودن مسیر ریشه پروژه به sys.path تا ایمپورت‌ها به درستی کار کنند
# This ensures that 'skymind_sim' can be imported as a top-level package
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# ایمپورت ماژول‌های پروژه پس از تنظیم path
from skymind_sim.config import load_config
from skymind_sim.utils.logger import setup_logging
from skymind_sim.layer_1_simulation.simulation import Simulation
from skymind_sim.layer_0_presentation.renderer import Renderer

# تعریف یک نام ثابت برای لاگر اصلی که از خطا جلوگیری می‌کند
MAIN_LOGGER_NAME = 'skymind_main'

def main():
    """
    نقطه ورود اصلی برنامه.
    کانفیگ را بارگیری کرده، لاگ‌گیری را تنظیم می‌کند، شبیه‌سازی و رندرکننده را
    راه‌اندازی کرده و حلقه اصلی برنامه را اجرا می‌کند.
    """
    # 1. بارگیری تنظیمات و پیکربندی لاگر
    config = load_config()
    setup_logging(config, main_logger_name=MAIN_LOGGER_NAME)
    main_logger = logging.getLogger(MAIN_LOGGER_NAME)

    try:
        main_logger.info("=" * 40)
        main_logger.info("  SkyMind Simulator Application Starting")
        main_logger.info("=" * 40)

        # 2. راه‌اندازی موتور شبیه‌سازی
        main_logger.info("Initializing simulation...")
        simulation = Simulation(config)

        # 3. راه‌اندازی موتور رندر (Pygame)
        main_logger.info("Initializing Pygame renderer...")
        renderer = Renderer(config)
        renderer.load_assets()

        # 4. ورود به حلقه اصلی برنامه
        main_logger.info("Starting the main application loop...")

        # نیازی به simulation.start() نیست. حلقه زیر کار را شروع می‌کند.
        
        running = True
        clock = pygame.time.Clock()

        while running:
            # --- بخش ۱: مدیریت ورودی و رویدادها (Event Handling) ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # TODO: مدیریت سایر رویدادها مانند ورودی کیبورد، کلیک ماوس و ...

            # --- بخش ۲: به‌روزرسانی منطق شبیه‌سازی (Update State) ---
            simulation.step()

            # --- بخش ۳: رندر کردن وضعیت فعلی (Render Frame) ---
            renderer.render(simulation.grid, simulation.entities)

            # --- بخش ۴: کنترل نرخ فریم (Frame Rate Control) ---
            # اطمینان از اینکه حلقه با سرعتی بیش از حد مشخص شده در کانفیگ اجرا نشود.
            clock.tick(int(config['renderer']['fps']))

    except Exception as e:
        # ثبت هرگونه خطای پیش‌بینی نشده که باعث توقف برنامه شود
        main_logger.critical(f"A fatal error occurred: {e}", exc_info=True)
    finally:
        # این بخش همیشه اجرا می‌شود، چه برنامه با موفقیت تمام شود چه با خطا
        main_logger.info("Shutting down SkyMind Simulator.")
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    main()
