# skymind_sim/utils/config_loader.py

import json
import os
from typing import Dict, Any

from skymind_sim.utils.log_manager import LogManager

logger = LogManager.get_logger(__name__)

class ConfigLoader:
    """
    کلاس Singleton برای بارگذاری و مدیریت فایل‌های تنظیمات JSON.
    این کلاس تضمین می‌کند که تنظیمات فقط یک بار بارگذاری شده و در کل برنامه
    به صورت یکسان در دسترس باشند.
    """
    _instance = None
    _configs: Dict[str, Any] = {}
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        # الگوی Singleton: اگر شیء ساخته نشده، آن را بساز
        if not cls._instance:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance

    @classmethod
    def initialize(cls, config_dir: str = 'data/config'):
        """
        این متد باید یک بار در ابتدای برنامه فراخوانی شود تا تنظیمات بارگذاری شوند.
        """
        if cls._is_initialized:
            logger.warning("ConfigLoader is already initialized. Skipping re-initialization.")
            return

        if not os.path.isdir(config_dir):
            logger.error(f"Configuration directory not found: {os.path.abspath(config_dir)}")
            raise FileNotFoundError(f"Configuration directory not found: {config_dir}")

        cls._load_all(config_dir)
        cls._is_initialized = True
        logger.info(f"✅ Configurations loaded successfully from: {os.path.abspath(config_dir)}")
        logger.info(f"   Loaded modules: {list(cls._configs.keys())}")


    @classmethod
    def _load_all(cls, config_dir: str):
        """
        تمام فایل‌های .json را از پوشه تنظیمات مشخص شده بارگذاری می‌کند.
        """
        cls._configs = {}
        for filename in os.listdir(config_dir):
            if filename.endswith(".json"):
                config_name = filename[:-5]  # حذف .json از نام فایل
                filepath = os.path.join(config_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        cls._configs[config_name] = json.load(f)
                except (json.JSONDecodeError, IOError) as e:
                    logger.error(f"Failed to load or parse config file {filepath}: {e}")

    @classmethod
    def get(cls, name: str) -> Dict[str, Any]:
        """
        تنظیمات مربوط به یک ماژول خاص را برمی‌گرداند.

        Args:
            name (str): نام ماژول تنظیمات (مثلاً 'window' یا 'grid').

        Returns:
            Dict[str, Any]: دیکشنری حاوی تنظیمات.
        
        Raises:
            KeyError: اگر تنظیمات با نام مورد نظر یافت نشود.
            RuntimeError: اگر ConfigLoader هنوز مقداردهی اولیه نشده باشد.
        """
        if not cls._is_initialized:
            # این حالت نباید رخ دهد اگر initialize در main فراخوانی شود
            # اما برای اطمینان اینجا قرار داده شده است.
            cls.initialize()
        
        try:
            return cls._configs[name]
        except KeyError:
            logger.error(f"Configuration '{name}' not found. Available configs: {list(cls._configs.keys())}")
            raise

    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """
        تمام تنظیمات بارگذاری شده را برمی‌گرداند.
        """
        if not cls._is_initialized:
            cls.initialize()
        return cls._configs
