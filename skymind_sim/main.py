import os
from .core.environment import Environment
from .core.simulation import Simulation
from .utils.log_manager import setup_logging, get_logger

# در ابتدای برنامه، سیستم لاگینگ را یک‌بار برای همیشه تنظیم می‌کنیم
setup_logging()

# یک لاگر برای همین فایل (main) دریافت می‌کنیم
# __name__ در اینجا به "__main__" تبدیل می‌شود
logger = get_logger(__name__)

def main():
    """
    The main entry point for the SkyMind Simulator.
    """
    logger.info("Starting SkyMind Simulator...")

    try:
        # تعریف مسیر فایل نقشه
        # با استفاده از os.path.join، کد در ویندوز و لینوکس به درستی کار می‌کند
        map_file_path = os.path.join("data", "maps", "multi_drone_map.txt")
        logger.info(f"Loading map from: {map_file_path}")

        # ایجاد محیط شبیه‌سازی
        env = Environment(map_file_path=map_file_path)
        
        # ایجاد و اجرای شبیه‌سازی
        sim = Simulation(env)
        sim.run()

        logger.info("Simulation finished successfully.")

    except FileNotFoundError:
        logger.error(f"Error: Map file not found at '{map_file_path}'. Please check the path.")
    except Exception as e:
        logger.critical(f"An unexpected critical error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
