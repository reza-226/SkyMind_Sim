# skymind_sim/main.py

import os
from .core.environment import Environment
from .core.path_planner import PathPlanner
from .core.simulation import Simulation

def get_map_path():
    """
    مسیر کامل فایل نقشه را پیدا می‌کند.
    این تابع فرض می‌کند که فایل نقشه در پوشه 'data/maps' قرار دارد.
    """
    # مسیر ریشه پروژه را پیدا می‌کند (جایی که .git یا فایل اصلی پروژه قرار دارد)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    map_filename = "basic_map.json"  # نام فایل نقشه
    map_path = os.path.join(project_root, 'data', 'maps', map_filename)
    return map_path

def main():
    """
    نقطه ورود اصلی برنامه.
    محیط را بارگذاری می‌کند، مسیریابی را انجام می‌دهد و شبیه‌سازی را اجرا می‌کند.
    """
    print("Starting SkyMind Simulation...")

    # --- مرحله 1: بارگذاری محیط ---
    map_path = get_map_path()
    if not os.path.exists(map_path):
        print(f"FATAL ERROR: Map file not found at '{map_path}'")
        print("Please ensure 'basic_map.json' exists in the 'data/maps' directory.")
        return

    # ----- این بخش تغییر کرده است -----
    # 1. یک نمونه خالی از محیط ایجاد می‌کنیم
    env = Environment()
    
    # 2. متد load_from_json را روی نمونه созда شده فراخوانی می‌کنیم
    # رزولوشن را می‌توان به صورت یک پارامتر در فایل JSON اضافه کرد
    # اما برای سادگی، فعلاً آن را اینجا نگه می‌داریم
    success = env.load_from_json(map_path) 
    
    if not success:
        print("Failed to initialize environment. Exiting.")
        return
    # ------------------------------------

    # --- مرحله 2: برنامه‌ریزی مسیر ---
    print("\nStarting Path Planning...")
    # ایجاد یک نمونه از PathPlanner با محیط بارگذاری شده
    planner = PathPlanner(env)

    # پیدا کردن مسیر از نقطه شروع به پایان
    path = planner.find_path()

    if path:
        print(f"Path found with {len(path)} points.")
        # برای مشاهده، می‌توان مسیر را چاپ کرد
        # print("Path coordinates:", path)
    else:
        print("Could not find a path. Exiting.")
        return

    # --- مرحله 3: اجرای شبیه‌سازی (در آینده تکمیل می‌شود) ---
    print("\nPath planning successful. Simulation setup can now proceed.")
    # sim = Simulation(env, path)
    # sim.run()

    print("\nMain execution finished.")


if __name__ == "__main__":
    main()
