# =========================================================================
#  File: skymind_sim/config.py
#  Author: Reza & AI Assistant | 2025-10-14 (Final Version)
# =========================================================================
import configparser
import os
import logging
import json
from typing import Dict, Any

logger = logging.getLogger(__name__)

def load_config(config_path: str = 'config.ini') -> Dict[str, Any]:
    """
    فایل پیکربندی (ini) را از مسیر مشخص شده می‌خواند و آن را به یک
    دیکشنری پایتون تبدیل می‌کند.
    انکودینگ UTF-8 برای پشتیبانی از کاراکترهای فارسی پشتیبانی می‌شود.
    """
    project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    absolute_config_path = os.path.join(project_root_dir, config_path)
    absolute_config_path = os.path.normpath(absolute_config_path)

    print(f"\nDEBUG: Attempting to read config from absolute path: {absolute_config_path}\n")

    if not os.path.exists(absolute_config_path):
        logger.critical(f"Configuration file not found at: {absolute_config_path}")
        return {}

    config_parser = configparser.ConfigParser()
    try:
        # مشخص کردن انکودینگ UTF-8 برای جلوگیری از خطای UnicodeDecodeError
        config_parser.read(absolute_config_path, encoding='utf-8')

        # تبدیل شیء ConfigParser به یک دیکشنری استاندارد
        config_dict: Dict[str, Any] = {
            section: dict(config_parser.items(section))
            for section in config_parser.sections()
        }

        # چاپ محتوای تبدیل شده برای دیباگ
        print("--- DEBUG: Content converted to Python dictionary ---")
        print(json.dumps(config_dict, indent=4, ensure_ascii=False))
        print("---------------------------------------------------\n")

        return config_dict

    except configparser.Error as e:
        logger.critical(f"Error parsing configuration file '{absolute_config_path}': {e}")
        return {}
    except UnicodeDecodeError as e:
        logger.critical(f"Encoding error in '{absolute_config_path}'. Ensure it's saved as UTF-8. Error: {e}")
        return {}
