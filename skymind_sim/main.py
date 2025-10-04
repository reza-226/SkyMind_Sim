import os
import json
from skymind_sim.utils.logger import setup_logging
import logging
from skymind_sim.layer_1_simulation.simulation import Simulation

# --- راه‌اندازی لاگر ---
setup_logging(level="INFO", log_file="data/simulation_logs/simulation.log")
logger = logging.getLogger("SkyMind")


def load_json(file_path):
    """لود ساده یک فایل JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"خطا در خواندن {file_path}: {e}")
        raise


def main():
    logger.info("Initializing SkyMind Simulation...")

    # مسیر پایه داده‌ها
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

    # --- خواندن کل فایل کانفیگ ---
    config_all = load_json(os.path.join(data_dir, "config", "simulation.json"))

    # استخراج بخش‌ها
    map_data = config_all["map_data"]
    drone_configs = config_all["drone_configs"]
    simulation_config = config_all["simulation_config"]

    # تضمین وجود map_path
    if "map_path" not in simulation_config:
        simulation_config["map_path"] = map_data.get("grid", "data/maps/multi_drone_map.txt")

    # --- ساخت شبیه‌ساز ---
    simulation = Simulation(
        map_data=map_data,
        drone_configs=drone_configs,
        simulation_config=simulation_config
    )

    logger.info("Starting simulation...")
    simulation.run()


if __name__ == "__main__":
    main()
