# skymind_sim/main.py

import numpy as np
from .core.drone import Drone
from .core.environment import Environment, BoxObstacle
from .core.simulation import Simulation

def main():
    """
    نقطه ورود اصلی برای اجرای شبیه‌سازی.
    """
    # تعریف ابعاد محیط (۱۰x۱۰x۵ متر)
    env_dims = (10, 10, 5)

    # تعریف موانع
    obstacles = [
        BoxObstacle(position=np.array([5, 5, 2.5]), size=np.array([2, 2, 5])),
        BoxObstacle(position=np.array([2, 8, 2]), size=np.array([3, 1, 4]))
    ]

    # ایجاد محیط با موانع
    env = Environment(dimensions=env_dims, obstacles=obstacles)

    # --- تعریف پهپادها با نقاط شروع و پایان ---
    # این پهپاد باید از مانع بزرگ وسطی عبور کند
    drone1 = Drone(start_pos=np.array([1, 1, 1]), goal_pos=np.array([9, 9, 1]))
    
    # این پهپاد باید از هر دو مانع عبور کند
    drone2 = Drone(start_pos=np.array([1, 9, 4]), goal_pos=np.array([9, 1, 4]))
    # -------------------------------------------

    # اضافه کردن پهپادها به محیط
    env.add_drone(drone1)
    env.add_drone(drone2)

    # ایجاد و اجرای شبیه‌سازی
    sim = Simulation(env)
    sim.run()

if __name__ == "__main__":
    main()
