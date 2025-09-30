# skymind_sim/main.py

import json
import os
import traceback  # برای چاپ جزئیات خطا

# ایمپورت ماژول‌های پروژه
from skymind_sim.core.environment import Environment
from skymind_sim.core.path_planner import PathPlanner
from skymind_sim.core.drone import Drone
from skymind_sim.core.simulation import Simulation

def main():
    """
    نقطه شروع اصلی برای اجرای شبیه‌ساز پهپاد SkyMind.
    این تابع وظایف زیر را به ترتیب انجام می‌دهد:
    1. بارگذاری نقشه و ایجاد محیط شبیه‌سازی.
    2. استخراج نقاط شروع و پایان.
    3. برنامه‌ریزی مسیر با استفاده از الگوریتم A*.
    4. در صورت یافتن مسیر، راه‌اندازی و اجرای شبیه‌سازی حرکت پهپاد.
    """
    map_filename = 'simple_map.json'
    map_filepath = os.path.join('data', 'maps', map_filename)

    try:
        # -----------------------------------------------------------------
        # STEP 1: Load Map and Create Environment
        # -----------------------------------------------------------------
        print(f"--- STEP 1: Loading map from '{map_filepath}' ---")
        if not os.path.exists(map_filepath):
            raise FileNotFoundError(f"Map file not found at the specified path: {map_filepath}")

        with open(map_filepath, 'r') as f:
            map_data = json.load(f)
        
        env = Environment(map_data)
        print("Environment created successfully.")
        print(f"Map Dimensions: {env.dimensions}")
        print(f"Number of Obstacles: {len(env.obstacles)}")

        # -----------------------------------------------------------------
        # STEP 2: Extract Start and End Points
        # -----------------------------------------------------------------
        print("\n--- STEP 2: Extracting Start and End Points ---")
        # استخراج صحیح موقعیت‌ها از ساختار JSON نقشه
        start_position_list = env.map_data['start_points'][0]['position']
        start_point = tuple(start_position_list)
        
        end_position_list = env.map_data['end_points'][0]['position']
        end_point = tuple(end_position_list)
        
        print(f"Start Point: {start_point}")
        print(f"End Point: {end_point}")

        # -----------------------------------------------------------------
        # STEP 3: Plan Path using A*
        # -----------------------------------------------------------------
        print("\n--- STEP 3: Planning Path using A* Algorithm ---")
        planner = PathPlanner(env)
        path = planner.plan_path(start_point, end_point)

        # -----------------------------------------------------------------
        # STEP 4: Initialize and Run Simulation (if path is found)
        # -----------------------------------------------------------------
        if path:
            print(f"\nPath successfully found with {len(path)} waypoints.")
            print(f"Start: {path[0]}, End: {path[-1]}")
            
            # نمایش نمونه‌ای از مسیر برای بررسی سریع
            path_sample = path[:3] + ["..."] + path[-3:] if len(path) > 6 else path
            print(f"Path sample: {path_sample}")

            print("\n--- STEP 4: Initializing and Running Simulation ---")
            
            # ایجاد یک نمونه پهپاد در نقطه شروع
            drone = Drone(start_point=start_point)

            # ایجاد یک نمونه شبیه‌سازی با محیط و پهپاد
            sim = Simulation(environment=env, drone=drone)

            # اجرای شبیه‌سازی با مسیر یافت‌شده
            # آرگومان دوم، سرعت شبیه‌سازی است (تاخیر بین هر گام به ثانیه)
            # مقدار کمتر = شبیه‌سازی سریع‌تر
            sim.run(path=path, simulation_speed=0.05)

        else:
            print("\nCould not find a path to the destination. The simulation will not run.")

    except FileNotFoundError as e:
        print(f"\n[ERROR] A critical file was not found: {e}")
        print("Please ensure that the map file exists and the path is correct.")
        
    except (KeyError, IndexError) as e:
        print(f"\n[ERROR] Map data is malformed or missing key information: {e}")
        print("Please check the structure of your JSON map file for 'start_points', 'end_points', or 'obstacles'.")

    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")
        print("--- Traceback ---")
        traceback.print_exc() # چاپ جزئیات کامل خطا برای دیباگ

if __name__ == "__main__":
    main()
