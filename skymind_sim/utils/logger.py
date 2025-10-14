# skymind_sim/utils/logger.py
import logging
import sys
from logging.handlers import RotatingFileHandler

class LogManager:
    _loggers = {}
    _initialized = False

    @staticmethod
    def _initialize():
        if LogManager._initialized:
            return

        # تنظیمات کلی برای root logger
        log_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Handler برای چاپ در کنسول (stdout)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(log_format)

        # Handler برای نوشتن در فایل با قابلیت چرخش
        # فایل در پوشه data/simulation_logs ذخیره می‌شود.
        file_handler = RotatingFileHandler(
            'data/simulation_logs/simulation.log', 
            maxBytes=5*1024*1024, # 5 MB
            backupCount=2
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)

        # اضافه کردن handlerها به root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG) # حداقل سطح برای ثبت لاگ
        root_logger.addHandler(stream_handler)
        root_logger.addHandler(file_handler)

        LogManager._initialized = True
        root_logger.info("LogManager initialized successfully.")


    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        یک لاگر با نام مشخص دریافت یا ایجاد می‌کند.
        """
        if not LogManager._initialized:
            LogManager._initialize()

        if name not in LogManager._loggers:
            LogManager._loggers[name] = logging.getLogger(name)
        
        return LogManager._loggers[name]
