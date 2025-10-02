# skymind_sim/layer_1_simulation/simulation.py
import time
from typing import Dict, Any, List

# وارد کردن کلاس‌ها از مسیرهای جدید و دقیق در لایه ۱
from skymind_sim.layer_1_simulation.entities.drone import Drone
from skymind_sim.layer_1_simulation.world.obstacle import Obstacle
# نکته: اگر scheduler.py در همین پوشه است، import آن به صورت نسبی کار می‌کند
# from .scheduler import Scheduler 

class Simulation:
    def __init__(self):
        self.drones: List[Drone] = []
        self.obstacles: List[Obstacle] = []
        self.start_time: float = 0.0
        self.sim_time: float = 0.0
        print("Simulation (Layer 1) initialized.")

    def setup_world(self):
        """یک دنیای ساده برای تست اولیه ایجاد می‌کند."""
        # ایجاد یک پهپاد در موقعیت (100, 100)
        drone1 = Drone(drone_id="d1", initial_position=(100, 100))
        # یک مسیر ساده برای حرکت به پهپاد می‌دهیم
        drone1.set_path([(100, 100), (700, 500), (700, 100), (100, 100)])
        self.drones.append(drone1)
        
        # ایجاد یک مانع در موقعیت (300, 200) با اندازه 50x150
        obstacle1 = Obstacle(obstacle_id="obs1", position=(300, 200), size=(50, 150))
        self.obstacles.append(obstacle1)
        
        print("World setup complete: 1 drone, 1 obstacle.")

    def start(self):
        """شبیه‌سازی را شروع می‌کند."""
        self.start_time = time.time()
        self.sim_time = 0.0
        print("Simulation started.")

    def update(self, dt: float):
        """
        وضعیت شبیه‌سازی را به اندازه dt (دلتا تایم) به جلو می‌برد.
        """
        self.sim_time += dt
        for drone in self.drones:
            drone.update(dt)

    def get_world_state(self) -> Dict[str, Any]:
        """
        یک دیکشنری از وضعیت فعلی دنیای شبیه‌سازی برای لایه‌های دیگر (مثل لایه نمایش) برمی‌گرداند.
        """
        return {
            "time": self.sim_time,
            "drones": [d.get_state() for d in self.drones],
            "obstacles": [o.get_state() for o in self.obstacles]
        }
