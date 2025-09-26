# skymind_sim/main.py

import time
from .core.environment import Environment
from .core.drone import Drone
from .core.simulation import Simulation
from .utils.pathfinding import a_star_search
from .utils.logger import setup_logger

def main():
    """
    تابع اصلی برای اجرای شبیه‌سازی.
    """
    try:
        print("--- SkyMind Simulation Initializing ---")
        
        # راه‌اندازی لاگر
        logger = setup_logger("simulation_log", "data/simulation_logs/sim.log")
        logger.info("Simulation started.")

        # ایجاد محیط از روی فایل نقشه
        # آرگومان‌های width و height حذف شده‌اند چون از فایل خوانده می‌شوند
        env = Environment(map_file_path="data/maps/complex_map_01.txt")
        logger.info(f"Environment loaded with map: data/maps/complex_map_01.txt")

        # ایجاد پهپاد و افزودن آن به محیط
        drone1 = Drone(drone_id="Alpha-1", position=env.start_pos)
        env.add_drone(drone1)
        logger.info(f"Drone '{drone1.drone_id}' created at position {drone1.position}")

        # پیدا کردن مسیر با استفاده از A*
        path = a_star_search(env.grid, env.start_pos, env.end_pos)
        
        if not path:
            print("No path found from Start to End!")
            logger.warning("Pathfinding failed. No path found.")
            return
        
        print(f"Path found with {len(path)} steps.")
        logger.info(f"Path found from {env.start_pos} to {env.end_pos} with {len(path)} steps.")
        drone1.set_path(path)

        # ایجاد و اجرای شبیه‌سازی
        sim = Simulation(env)
        sim.run()

        logger.info("Simulation finished successfully.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if 'logger' in locals():
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
