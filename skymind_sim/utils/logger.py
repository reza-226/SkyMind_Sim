# skymind_sim/utils/logger.py
import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(level: str = "INFO", log_file: str = "simulation.log"):
    """
    سیستم لاگ‌گیری پروژه را با قابلیت چرخش فایل‌ها تنظیم می‌کند.

    Args:
        level (str): سطح لاگ‌گیری (مانند 'DEBUG', 'INFO', 'WARNING', 'ERROR').
        log_file (str): مسیر فایل لاگ.
    """
    # اطمینان از وجود دایرکتوری لاگ
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # تبدیل سطح لاگ از رشته به مقدار عددی
    log_level = getattr(logging, level.upper(), logging.INFO)

    # تعریف فرمت پیام‌های لاگ
    log_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # گرفتن لاگر اصلی (root logger)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # پاک کردن handler های قبلی برای جلوگیری از لاگ تکراری
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # ایجاد handler برای کنسول (نمایش در ترمینال)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)

    # ایجاد handler برای فایل با قابلیت چرخش
    # فایل‌ها تا 5 مگابایت رشد می‌کنند و 5 فایل پشتیبان نگهداری می‌شود
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5*1024*1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    logging.info(f"سیستم لاگ‌گیری با موفقیت تنظیم شد. سطح لاگ: {level}, فایل لاگ: {log_file}")
