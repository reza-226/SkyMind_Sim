# =========================================================================
#  File: run_and_visualize.py
#  Author: Reza & AI Assistant | 2025-10-14 (Updated for Main Loop)
#  Description: Main entry point to run the simulation with visualization.
# =========================================================================

import logging
import sys
import os
import pygame  # <--- ایمپورت pygame برای مدیریت حلقه

# افزودن مسیر ریشه پروژه به sys.path برای ایمپورت‌های ماژولار
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from skymind_sim.utils.logger import setup_logging
from skymind_sim.config import load_config
from skymind_sim.layer_1_simulation.simulation import Simulation
from skymind_sim.layer_0_presentation.renderer import Renderer

# تعریف نام اصلی لاگر
MAIN_LOGGER_NAME = "skymind_main"

def main():
    """
    تابع اصلی برای راه‌اندازی و اجرای شبیه‌سازی.
    """
    # بارگذاری کانفیگ و راه‌اندازی لاگر
    config = load_config()
    setup_logging(config, main_logger_name=MAIN_LOGGER_NAME)
    
    main_logger = logging.getLogger(MAIN_LOGGER_NAME)
    
    main_logger.info("========================================")
    main_logger.info("  SkyMind Simulator Application Starting  ")
    main_logger.info("========================================")

    try:
        # ۱. ساخت شبیه‌ساز
        main_logger.info("Initializing simulation...")
        simulation = Simulation(config)

        # ۲. ساخت رندرکننده
        main_logger.info("Initializing Pygame renderer...")
        renderer = Renderer(config)
        renderer.load_assets() # بارگذاری تصاویر و فونت‌ها

        # ۳. حلقه اصلی برنامه
        main_logger.info("Starting the main application loop...")
        
        # استفاده از ساعت Pygame برای کنترل نرخ فریم
        clock = pygame.time.Clock()
        running = True
        
        while running:
            # مدیریت رویدادها (مانند بستن پنجره)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # >>> بخش کلیدی جدید <<<
            # اجرای یک گام از منطق شبیه‌سازی
            simulation.step()

            # رندر کردن وضعیت فعلی شبیه‌سازی
            renderer.render(simulation.grid, simulation.scheduler.agents)
            
            # کنترل نرخ فریم (مثلاً 30 فریم بر ثانیه)
            clock.tick(renderer.fps)

    except (ValueError, FileNotFoundError) as e:
        main_logger.error(f"A critical error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        main_logger.critical(f"An unexpected critical error occurred: {e}", exc_info=True)
        sys.exit(1)
    finally:
        main_logger.info("Shutting down SkyMind Simulator.")
        pygame.quit()

if __name__ == "__main__":
    main()
