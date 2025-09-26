# skymind_sim/main.py

# کلاس‌های مورد نیاز را وارد می‌کنیم
from .core.drone import Drone
from .core.environment import Environment

def run_simulation():
    """
    نقطه ورود اصلی برای اجرای شبیه‌سازی.
    """
    print("=========================================")
    print("  Initializing SkyMind Simulation...")
    print("=========================================")

    # -- ۱. ایجاد محیط شبیه‌سازی --
    print("\n--- Step 1: Creating the Environment ---")
    sim_environment = Environment(width=20, height=15)
    
    # چند مانع اضافه می‌کنیم
    sim_environment.add_obstacle((5, 5))
    sim_environment.add_obstacle((5, 6))
    sim_environment.add_obstacle((5, 7))

    # -- ۲. ایجاد پهپادها و افزودن به محیط --
    print("\n--- Step 2: Creating and Placing Drones ---")
    try:
        # ایجاد دو پهپاد
        drone1 = Drone(drone_id="Alpha-1", start_position=(2, 2))
        drone2 = Drone(drone_id="Beta-2", start_position=(18, 13))

        # افزودن پهپادها به محیط
        sim_environment.add_drone(drone1)
        sim_environment.add_drone(drone2)
        
        # تست یک مورد خطا: تلاش برای افزودن پهپاد روی یک مانع
        drone3_on_obstacle = Drone(drone_id="Gamma-3", start_position=(5, 5))
        sim_environment.add_drone(drone3_on_obstacle)

    except ValueError as e:
        print(f"[ERROR] {e}")


    # -- ۳. نمایش وضعیت اولیه محیط --
    sim_environment.display()
    
    # -- ۴. اجرای یک دستور ساده --
    print("\n--- Step 3: Executing a simple command ---")
    # به یکی از پهپادها دستور حرکت می‌دهیم
    drone_to_move = sim_environment.drones[0] # انتخاب اولین پهپاد (Alpha-1)
    new_pos = (8, 8)
    if sim_environment.is_valid_position(new_pos):
        drone_to_move.move_to(new_pos)
    
    # -- ۵. نمایش وضعیت نهایی محیط --
    sim_environment.display()


if __name__ == "__main__":
    run_simulation()
