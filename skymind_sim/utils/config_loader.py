# مسیر: skymind_sim/utils/config_loader.py
import json
import os
import logging

DEFAULT_CONFIGS = {
    "window.json": {"width": 800, "height": 600, "fullscreen": False},
    "grid.json": {"rows": 20, "cols": 20, "cell_size": 32},
    "simulation.json": {"speed": 1.0, "max_drones": 5}
}

def load_json_config(file_path: str) -> dict:
    """
    خواندن و اعتبارسنجی فایل کانفیگ JSON.
    اگر فایل نبود یا خراب بود، هشدار داده و از کانفیگ پیش‌فرض استفاده می‌کند.
    """
    filename = os.path.basename(file_path)
    if not os.path.exists(file_path):
        logging.warning(f"فایل کانفیگ یافت نشد: {file_path} — استفاده از پیش‌فرض.")
        return DEFAULT_CONFIGS.get(filename, {})

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logging.info(f"کانفیگ با موفقیت بارگذاری شد: {file_path}")
            return data
    except json.JSONDecodeError as e:
        logging.warning(f"خطا در پارس فایل JSON ({file_path}): {e} — استفاده از پیش‌فرض.")
        return DEFAULT_CONFIGS.get(filename, {})

def load_all_configs(config_dir: str) -> tuple:
    """
    بارگذاری همه کانفیگ‌ها از مسیر مشخص‌شده.
    """
    window_config = load_json_config(os.path.join(config_dir, "window.json"))
    grid_config = load_json_config(os.path.join(config_dir, "grid.json"))
    simulation_config = load_json_config(os.path.join(config_dir, "simulation.json"))
    return window_config, grid_config, simulation_config
