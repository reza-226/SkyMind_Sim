# skymind_sim/config.py
import json
import logging
import os

def load_config(path: str) -> dict:
    """
    یک فایل پیکربندی JSON را از مسیر مشخص شده بارگذاری می‌کند.

    Args:
        path (str): مسیر فایل config.json.

    Returns:
        dict: دیکشنری حاوی تنظیمات.
    
    Raises:
        FileNotFoundError: اگر فایل پیدا نشود.
        json.JSONDecodeError: اگر فایل JSON معتبر نباشد.
    """
    if not os.path.exists(path):
        logging.error(f"فایل پیکربندی در مسیر '{os.path.abspath(path)}' یافت نشد.")
        raise FileNotFoundError(f"Configuration file not found at: {os.path.abspath(path)}")

    try:
        with open(path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logging.info(f"پیکربندی با موفقیت از '{os.path.abspath(path)}' بارگذاری شد.")
        return config
    except json.JSONDecodeError as e:
        logging.error(f"خطا در پارس کردن فایل JSON پیکربندی: '{os.path.abspath(path)}'. جزئیات: {e}")
        raise
    except Exception as e:
        logging.critical(f"یک خطای پیش‌بینی نشده هنگام بارگذاری کانفیگ از '{os.path.abspath(path)}' رخ داد: {e}")
        raise
