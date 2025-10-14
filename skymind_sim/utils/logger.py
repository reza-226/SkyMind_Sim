# =========================================================================
#  File: skymind_sim/utils/logger.py
#  Author: Reza & AI Assistant | 2025-10-14 (Final Corrected Version)
# =========================================================================
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Dict, Any

# یک متغیر برای جلوگیری از تنظیم چندباره لاگر ریشه
_is_root_configured = False

def setup_logging(config: Dict[str, Any], main_logger_name: str):
    """
    سیستم لاگ‌گیری را بر اساس تنظیمات پیکربندی می‌کند.
    این تابع باید فقط یک بار در ابتدای برنامه فراخوانی شود.

    Args:
        config (Dict[str, Any]): دیکشنری کامل تنظیمات.
        main_logger_name (str): نام لاگر اصلی برنامه (مثلاً 'skymind_main').
    """
    global _is_root_configured
    if _is_root_configured:
        # اگر لاگر قبلاً تنظیم شده، فقط یک هشدار می‌دهیم و خارج می‌شویم.
        # این کار از لاگ‌های تکراری جلوگیری می‌کند.
        logging.getLogger(main_logger_name).debug("setup_logging called more than once. Skipping reconfiguration.")
        return

    try:
        log_config = config['logging']
        log_level_str = log_config.get('log_level', 'INFO').upper()
        log_file_path = log_config.get('log_file', 'data/logs/default.log')
        log_level = getattr(logging, log_level_str, logging.INFO)

    except KeyError:
        # اگر بخش 'logging' در کانفیگ نباشد، از تنظیمات پایه استفاده می‌کنیم.
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logging.warning("Logging configuration section not found. Using default INFO level.")
        _is_root_configured = True
        return

    # ایجاد دایرکتوری لاگ در صورت عدم وجود
    log_dir = os.path.dirname(log_file_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    
    # فرمت لاگ
    log_format = '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

    # تنظیم لاگر ریشه (Root Logger)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # پاک کردن handlerهای قبلی برای جلوگیری از تکرار لاگ
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Handler برای نمایش لاگ در کنسول
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Handler برای ذخیره لاگ در فایل با قابلیت چرخش
    # 5MB per file, keep 3 backup files
    file_handler = RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    _is_root_configured = True
    
    # لاگ اولیه برای تایید صحت عملکرد
    logger = logging.getLogger(main_logger_name)
    logger.info(f"Logger '{main_logger_name}' configured with level {log_level_str}.")
    logger.info(f"Log output will be saved to: {os.path.abspath(log_file_path)}")
