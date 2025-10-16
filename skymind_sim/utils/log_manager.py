# skymind_sim/utils/log_manager.py

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class LogManager:
    """
    یک کلاس استاتیک برای مدیریت متمرکز لاگر در کل پروژه.
    """
    _logger_initialized = False
    _log_directory = "data/simulation_logs"
    _log_level = logging.INFO
    _log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    @staticmethod
    def init_logger():
        """
        لاگر اصلی برنامه را مقداردهی اولیه می‌کند.
        این متد باید فقط یک بار در ابتدای برنامه فراخوانی شود.
        """
        if LogManager._logger_initialized:
            return

        # ایجاد پوشه لاگ در صورت عدم وجود
        os.makedirs(LogManager._log_directory, exist_ok=True)

        # ایجاد نام فایل لاگ بر اساس تاریخ و زمان فعلی
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"simulation_{timestamp}.log"
        log_file_path = os.path.join(LogManager._log_directory, log_filename)

        # تنظیمات اصلی لاگر
        root_logger = logging.getLogger()
        root_logger.setLevel(LogManager._log_level)

        formatter = logging.Formatter(LogManager._log_format)

        # Handler برای نمایش لاگ‌ها در کنسول
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        # Handler برای ذخیره لاگ‌ها در فایل با قابلیت چرخش (rotation)
        # فایل‌ها بعد از رسیدن به حجم 5MB، تا 5 نسخه پشتیبان خواهند داشت
        file_handler = RotatingFileHandler(
            log_file_path, maxBytes=5*1024*1024, backupCount=5
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

        LogManager._logger_initialized = True
        
        # لاگ اولیه برای تایید صحت عملکرد
        initial_logger = logging.getLogger(__name__)
        initial_logger.info(f"Logger initialized. Log file: {log_file_path}")


    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        یک نمونه لاگر برای ماژول مشخص شده برمی‌گرداند.

        Args:
            name (str): نام ماژول که معمولاً __name__ است.

        Returns:
            logging.Logger: نمونه لاگر برای استفاده.
        """
        if not LogManager._logger_initialized:
            # اگر لاگر هنوز init نشده، یک هشدار نمایش می‌دهد و آن را init می‌کند
            # این کار برای جلوگیری از خطاهای احتمالی است
            print("WARNING: Logger was not explicitly initialized. Auto-initializing now.")
            LogManager.init_logger()
            
        return logging.getLogger(name)
