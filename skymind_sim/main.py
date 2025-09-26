# skymind_sim/main.py

import time
from .core.environment import Environment
from .core.drone import Drone
from .core.simulation import Simulation

def run_simulation():
    """
    تابع اصلی برای تنظیم و اجرای شبیه‌سازی.
    """
    print("=========================================")
    print("  Setting up Simulation Scenario...")
    print("=========================================")

    # 1. ساخت محیط شبیه‌سازی
    sim_environment = Environment(width=15, height=10)

    # 2. افزودن موانع
    # ایجاد یک دیوار عمودی
    for y in range(3, 7):
        sim_environment.add_obstacle((7, y))
        
    # 3. ساخت و افزودن پهپادها
    # موقعیت اولیه Alpha-1 با توجه به خروجی شما (1,1) در نظر گرفته شد.
    drone1 = Drone(drone_id="Alpha-1", start_position=(1, 1), speed=1)
    drone2 = Drone(drone_id="Beta-2", start_position=(13, 8), speed=1)
    
    sim_environment.add_drone(drone1)
    sim_environment.add_drone(drone2)
    
    print("\n--- Initial Environment State ---")
    sim_environment.display()

    # 4. ساخت موتور شبیه‌سازی
    simulation_engine = Simulation(sim_environment)

    # 5. دادن دستورات اولیه به پهپادها
    # یک پهپاد را برای دادن دستور پیدا می‌کنیم
    alpha_drone = None
    for drone in sim_environment.drones:
        if drone.drone_id == 'Alpha-1':
            alpha_drone = drone
            break
    
    if alpha_drone:
        # دستور حرکت به مقصد جدید
        alpha_drone.move_to((12, 8))
    
    # 6. اجرای شبیه‌سازی
    simulation_engine.run(max_ticks=25, tick_duration=0.3)


if __name__ == "__main__":
    run_simulation()
