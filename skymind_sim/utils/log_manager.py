# skymind_sim/utils/log_manager.py

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime

class LogManager:
    """
    کلاس Singleton برای مدیریت سراسری لاگ‌ها در برنامه.
    این کلاس سیستم لاگینگ را با تنظیمات مشخص شده مقداردهی اولیه می‌کند
    و یک متد استاتیک برای دریافت لاگر برای هر ماژول فراهم می‌کند.
    """
    _is_initialized = False

    @classmethod
    def initialize(cls):
        """
        سیستم لاگینگ را بر اساس تنظیمات فایل پیکربندی، مقداردهی اولیه می‌کند.
        این متد باید یک بار در ابتدای برنامه فراخوانی شود.
        """
        if cls._is_initialized:
            return

        # <<<<< تغییر کلیدی: ایمپورت محلی برای شکستن چرخه وابستگی >>>>>
        from skymind_sim.utils.config_loader import ConfigLoader

        try:
            log_config = ConfigLoader.get('logging')
            log_dir = log_config.get("log_directory", "data/simulation_logs")
            log_level_str = log_config.get("level", "INFO").upper()
            log_filename = log_config.get("filename", "simulation.log")
            
            # تبدیل نام سطح لاگ به مقدار عددی متناظر
            log_level = getattr(logging, log_level_str, logging.INFO)

            # اطمینان از وجود پوشه لاگ‌ها
            os.makedirs(log_dir, exist_ok=True)
            
            # ایجاد نام فایل منحصر به فرد با timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_log_filename = f"{log_filename.split('.')[0]}_{timestamp}.log"
            log_path = os.path.join(log_dir, unique_log_filename)

            # ایجاد یک فرمت استاندارد برای لاگ‌ها
            log_format = logging.Formatter(
                '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'
            )

            # تنظیم لاگر ریشه (Root Logger)
            root_logger = logging.getLogger()
            root_logger.setLevel(log_level)
            
            # حذف handlerهای قبلی برای جلوگیری از لاگ‌های تکراری
            if root_logger.hasHandlers():
                root_logger.handlers.clear()

            # ۱. Handler برای چاپ لاگ‌ها در کنسول (stdout)
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(log_format)
            root_logger.addHandler(console_handler)

            # ۲. Handler برای ذخیره لاگ‌ها در فایل (با چرخش)
            # فایل‌ها پس از رسیدن به حجم 1MB چرخش پیدا می‌کنند و تا 5 فایل پشتیبان نگهداری می‌شود.
            file_handler = RotatingFileHandler(
                log_path, maxBytes=1*1024*1024, backupCount=5, encoding='utf-8'
            )
            file_handler.setFormatter(log_format)
            root_logger.addHandler(file_handler)

            cls._is_initialized = True
            
            # اولین پیام لاگ پس از مقداردهی اولیه موفقیت‌آمیز
            logging.info(f"LogManager initialized successfully. Log level: {log_level_str}. Logging to {log_path}")

        except (KeyError, FileNotFoundError) as e:
            # در صورت عدم وجود تنظیمات لاگ، یک لاگر پیش‌فرض راه‌اندازی می‌شود.
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
            logging.warning(f"Could not initialize LogManager from config. Using basic config. Reason: {e}")
            cls._is_initialized = True

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        یک نمونه لاگر برای ماژول مشخص شده برمی‌گرداند.

        Args:
            name (str): نام ماژول (معمولاً __name__).

        Returns:
            logging.Logger: نمونه لاگر پیکربندی شده.
        """
        return logging.getLogger(name)
