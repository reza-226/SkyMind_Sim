# skymind_sim/main.py

import os
from .core.environment import Environment
from .core.simulation import Simulation
from .core.drone import Drone
from .core.path_planner import PathPlanner

def main():
    """
    نقطه ورود اصلی برنامه شبیه‌ساز.
    """
    print("Loading map from 'data/maps/basic_map.json'...")
    
    # ساخت مسیر کامل به فایل نقشه
    # این کار باعث می‌شود برنامه از هر جایی که اجرا شود، فایل را پیدا کند.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(base_dir, '..', 'data', 'maps', 'basic_map.json')
    map_path = os.path.normpath(map_path)
    
    # ایجاد محیط از روی فایل نقشه
    env = Environment.from_json_file(map_path)
    if env is None:
        print("Failed to create environment. Exiting.")
        return
        
    print("Map loaded successfully.")

    # ایجاد یک نمونه از مسیریاب
    path_planner = PathPlanner(env)

    # برای هر پهپاد در محیط، یک مسیر پیدا کن (در آینده)
    for drone in env.drones:
        print(f"Planning path for Drone ID: {drone.id}...")
        
        # --- اصلاح کلیدی در این خط ---
        # نام متد از plan_path به find_path تغییر کرد
        path = path_planner.find_path(drone.start_position, drone.goal_position)
        # -----------------------------
        
        # در حال حاضر چون مسیریابی پیاده‌سازی نشده، path همیشه None خواهد بود.
        # در آینده این بخش کامل‌تر خواهد شد.

    # ایجاد و اجرای شبیه‌سازی
    sim = Simulation(env)
    print(f"Simulation created for {len(env.drones)} drones.")
    
    print("Starting simulation...")
    sim.run()
    print("Simulation finished.")

if __name__ == "__main__":
    main()
