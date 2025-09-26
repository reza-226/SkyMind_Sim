# skymind_sim/main.py

from .core.drone import Drone
from .core.environment import Environment
from .core.simulation import Simulation

def setup_scenario():
    """
    یک سناریوی اولیه برای شبیه‌سازی ایجاد و پیکربندی می‌کند.
    محیط، پهپادها و موانع را می‌سازد.
    """
    print("=========================================")
    print("  Setting up Simulation Scenario...")
    print("=========================================")

    # ۱. ایجاد محیط
    environment = Environment(width=15, height=10)
    
    # ۲. افزودن موانع
    environment.add_obstacle((7, 3))
    environment.add_obstacle((7, 4))
    environment.add_obstacle((7, 5))
    environment.add_obstacle((7, 6))

    # ۳. ایجاد پهپادها و افزودن به محیط
    try:
        drone1 = Drone(drone_id="Alpha-1", start_position=(1, 1))
        drone2 = Drone(drone_id="Beta-2", start_position=(13, 8))
        
        environment.add_drone(drone1)
        environment.add_drone(drone2)
    except ValueError as e:
        print(f"[ERROR] Could not set up drones: {e}")
        return None

    # نمایش وضعیت اولیه قبل از شروع شبیه‌سازی
    print("\n--- Initial Environment State ---")
    environment.display()
    
    return environment


def run_simulation():
    """
    نقطه ورود اصلی. سناریو را تنظیم کرده و موتور شبیه‌سازی را اجرا می‌کند.
    """
    # گام ۱: سناریو را آماده کن
    sim_environment = setup_scenario()
    
    if sim_environment is None:
        print("\n[FATAL] Failed to set up scenario. Aborting simulation.")
        return

    # گام ۲: موتور شبیه‌سازی را با محیط آماده شده، بساز
    simulation = Simulation(sim_environment)
    
    # گام ۳: شبیه‌سازی را برای تعداد محدودی تیک اجرا کن
    # ما اینجا فقط 5 تیک اجرا می‌کنیم تا خروجی خیلی طولانی نشود.
    simulation.run(max_ticks=5, tick_duration=0.5)


if __name__ == "__main__":
    run_simulation()
