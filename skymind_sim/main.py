# skymind_sim/main.py

import sys
import traceback
import pygame
from skymind_sim.utils.config_loader import ConfigLoader
from skymind_sim.utils.log_manager import LogManager
from skymind_sim.layer_1_simulation.simulation import Simulation

# این باید اولین چیزی باشد که اجرا می‌شود تا loggerها به درستی کار کنند
# و بتوانند فرآیند بارگذاری تنظیمات را نیز لاگ کنند.
LogManager.initialize()

# حالا که لاگر آماده است، یک لاگر برای این ماژول می‌گیریم
logger = LogManager.get_logger(__name__)

def main():
    """
    نقطه ورود اصلی برای اجرای شبیه‌ساز SkyMind.
    """
    try:
        # مقداردهی اولیه ماژول‌های اصلی
        
        # ۱. بارگذاری تمام تنظیمات
        # این متد باید قبل از ساخت هر شیئی که به تنظیمات نیاز دارد، فراخوانی شود.
        ConfigLoader.initialize(config_dir='data/config')

        # ۲. مقداردهی اولیه Pygame
        # بهتر است بعد از بارگذاری تنظیمات باشد، شاید تنظیماتی برای pygame هم داشته باشیم.
        pygame.init()
        
        # ۳. ایجاد و اجرای شبیه‌سازی
        # حالا که همه چیز آماده است، شبیه‌ساز را می‌سازیم.
        logger.info("Starting simulation...")
        sim = Simulation()
        sim.run()

    except Exception as e:
        # استفاده از لاگر برای ثبت خطاهای پیش‌بینی نشده
        logger.error(f"An unhandled exception occurred in main: {e}", exc_info=True)
        # exc_info=True به طور خودکار traceback را به لاگ اضافه می‌کند.
        
    finally:
        # اطمینان از خروج تمیز از برنامه
        pygame.quit()
        logger.info("Pygame has been quit. Simulation finished.")
        # sys.exit() به طور خودکار در پایان اسکریپت اصلی اتفاق می‌افتد،
        # مگر اینکه بخواهید با کد خاصی خارج شوید.


if __name__ == '__main__':
    main()
