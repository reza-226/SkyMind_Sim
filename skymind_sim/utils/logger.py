import logging
import os
from datetime import datetime

_log_configured = False

def setup_logging(log_level=logging.INFO, log_dir="data/simulation_logs"):
    """
    Configures the root logger for the entire application.

    This function sets up logging to both a file and the console. It ensures
    that it only runs once to avoid adding multiple handlers.

    Args:
        log_level (int): The minimum logging level to capture (e.g., logging.INFO).
        log_dir (str): The directory where log files will be stored.
    """
    global _log_configured
    if _log_configured:
        return

    # اطمینان از وجود پوشه لاگ‌ها
    os.makedirs(log_dir, exist_ok=True)

    # ساخت نام فایل لاگ بر اساس تاریخ و زمان
    log_filename = f"simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_path = os.path.join(log_dir, log_filename)

    # تعریف فرمت لاگ
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)

    # گرفتن لاگر اصلی
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # پاک کردن هندلرهای قبلی برای جلوگیری از لاگ‌های تکراری
    if logger.hasHandlers():
        logger.handlers.clear()

    # ایجاد FileHandler برای نوشتن لاگ‌ها در فایل
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # ایجاد StreamHandler برای نمایش لاگ‌ها در کنسول
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    _log_configured = True
    logging.info("Logging configured successfully.")
    logging.info(f"Log file created at: {log_path}")

def get_logger(name):
    """
    Returns a logger instance for a specific module.

    Args:
        name (str): The name of the logger, typically __name__ of the calling module.

    Returns:
        logging.Logger: A configured logger instance.
    """
    return logging.getLogger(name)
