# ============================================================
#  File: config_loader.py
#  Layer: Utils
#  Author: Reza – October 2025
# ============================================================

import json
import os
from skymind_sim.utils.logger import setup_logger

def load_map_config(file_path="data/maps/basic_map.json"):
    """
    بارگذاری فایل JSON نقشه.
    خروجی: دیکشنری شامل داده‌های پهپاد، موانع و اهداف.
    """
    logger = setup_logger("ConfigLoader")

    if not os.path.exists(file_path):
        logger.error(f"❌ فایل نقشه یافت نشد: {file_path}")
        raise FileNotFoundError(f"Map config not found: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"📁 نقشه با موفقیت لود شد: {file_path}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"❌ خطا در تجزیه JSON: {e}")
        raise

def load_simulation_config(sim_file="data/config/simulation.json"):
    """
    (اختیاری) بارگذاری پیکربندی شبیه‌سازی مثل Tmax و Δt.
    """
    if not os.path.exists(sim_file):
        return {"time_step": 0.1, "max_time": 60.0}

    with open(sim_file, "r", encoding="utf-8") as f:
        try:
            cfg = json.load(f)
            return cfg
        except Exception:
            return {"time_step": 0.1, "max_time": 60.0}
