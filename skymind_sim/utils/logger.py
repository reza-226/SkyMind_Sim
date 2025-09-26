# skymind_sim/utils/logger.py

import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_file: str, level=logging.INFO):
    """
    یک لاگر را با تنظیمات مشخص راه‌اندازی و پیکربندی می‌کند.

    این لاگر می‌تواند خروجی را هم در کنسول و هم در یک فایل با قابلیت چرخش
    (Rotating) ثبت کند.

    :param name: نام لاگر.
    :param log_file: مسیر کامل فایل لاگ.
    :param level: سطح لاگ (e.g., logging.INFO, logging.DEBUG).
    :return: شیء لاگر پیکربندی شده.
    """
    # اطمینان از وجود پوشه برای فایل لاگ
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # تعریف فرمت پیام‌های لاگ
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # ایجاد یک handler برای نوشتن لاگ‌ها در فایل
    # RotatingFileHandler باعث می‌شود وقتی فایل لاگ به حجم مشخصی رسید،
    # یک فایل جدید ایجاد شود و فایل‌های قدیمی بایگانی شوند.
    file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024*5, backupCount=5) # 5 MB per file
    file_handler.setFormatter(formatter)

    # ایجاد یک handler برای نمایش لاگ‌ها در کنسول
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # گرفتن شیء لاگر و تنظیم سطح آن
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # جلوگیری از اضافه شدن چندباره handlerها در صورت فراخوانی مجدد تابع
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
