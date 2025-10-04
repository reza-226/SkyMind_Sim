# -*- coding: utf-8 -*-
# مسیر: skymind_sim/config.py

import configparser
import logging
import os
import json
from typing import Any, Tuple

class ConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_file: str = 'config.ini'):
        if hasattr(self, '_initialized') and self._initialized:
            return

        self.config = configparser.ConfigParser(interpolation=None)

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(project_root, config_file)

        if not os.path.exists(config_path):
            logging.error(f"فایل تنظیمات در مسیر '{config_path}' یافت نشد.")
            raise FileNotFoundError(f"فایل تنظیمات در مسیر '{config_path}' یافت نشد.")

        self.config.read(config_path, encoding='utf-8')
        logging.info(f"تنظیمات با موفقیت از '{config_path}' بارگذاری شد.")
        self._initialized = True

    # --- متدهای عمومی ---
    def get(self, section: str, option: str, fallback: Any = None) -> Any:
        return self.config.get(section, option, fallback=fallback)

    def getint(self, section: str, option: str, fallback: Any = None) -> int:
        return self.config.getint(section, option, fallback=fallback)

    def getfloat(self, section: str, option: str, fallback: Any = None) -> float:
        return self.config.getfloat(section, option, fallback=fallback)

    def getboolean(self, section: str, option: str, fallback: Any = None) -> bool:
        return self.config.getboolean(section, option, fallback=fallback)

    def get_json(self, section: str, option: str, fallback: Any = None) -> Any:
        raw_value = self.get(section, option, fallback=fallback)
        if raw_value is None:
            return fallback
        try:
            return json.loads(raw_value)
        except json.JSONDecodeError as e:
            raise ValueError(f"مقدار JSON معتبر نیست برای [{section}] {option}: {e}")

    def get_tuple_int(self, section: str, option: str, fallback: Tuple[int, ...] = None) -> Tuple[int, ...]:
        """رشته عددی جداشده با ویرگول را به tuple[int,...] تبدیل می‌کند."""
        raw_value = self.get(section, option, fallback=None)
        if raw_value is None:
            return fallback
        try:
            return tuple(int(x.strip()) for x in raw_value.split(','))
        except ValueError as e:
            raise ValueError(f"مقدار tuple عددی معتبر نیست برای [{section}] {option}: {e}")

# نمونه Singleton سراسری
config = ConfigManager()
