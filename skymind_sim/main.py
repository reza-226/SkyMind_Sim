# skymind_sim/main.py
import logging
import os
from skymind_sim.config import load_config
from skymind_sim.utils.logger import setup_logging
# این import را از کامنت خارج کنید
from skymind_sim.layer_1_simulation.simulation import Simulation

def main():
    """
    نقطه ورود اصلی برنامه شبیه‌سازی.
    """
    # ------------------ بخش بارگذاری کانفیگ ------------------
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_path = os.path.join(project_root,'config.json')
    print(f"DEBUG: Attempting to load config from: {config_path}")
    try:
        config = load_config(config_path)
    except (FileNotFoundError, Exception) as e:
        logging.basicConfig(level="ERROR", format='%(asctime)s - %(levelname)s - %(message)s')
        logging.critical(f"بارگذاری پیکربندی از مسیر '{config_path}' با شکست مواجه شد. جزئیات: {e}", exc_info=True)
        logging.critical("اجرای برنامه به دلیل عدم وجود یا خطای فایل کانفیگ متوقف شد.")
        return

    # ------------------ بخش تنظیم لاگ‌گیری ------------------
    log_config = config.get("logging", {})
    setup_logging(
        level=log_config.get("level", "INFO"),
        log_file=os.path.join(project_root, log_config.get("file", "data/simulation_logs/sim.log"))
    )

    # ------------------ بخش اصلی برنامه ------------------
    try:
        logging.info("پیکربندی با موفقیت بارگذاری شد. شروع شبیه‌سازی...")
        
        # این دو خط را از کامنت خارج کنید
        simulation = Simulation(config)
        simulation.run()
        
        logging.info("شبیه‌سازی با موفقیت به پایان رسید.")

    except Exception as e:
        logging.critical(f"یک خطای پیش‌بینی نشده در حین اجرای شبیه‌سازی رخ داد: {e}", exc_info=True)

if __name__ == "__main__":
    main()
