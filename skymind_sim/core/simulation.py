# skymind_sim/core/simulation.py

import time

class Simulation:
    """
    موتور اصلی شبیه‌سازی که حلقه زمان را مدیریت می‌کند و وضعیت اشیاء را به‌روزرسانی می‌کند.
    """
    def __init__(self, environment):
        """
        سازنده کلاس Simulation.

        Args:
            environment (Environment): شیء محیط شبیه‌سازی.
        """
        self.env = environment
        self.drones = []
        self.is_running = False
        
        # dt: گام زمانی برای هر فریم شبیه‌سازی (مثلاً 0.1 ثانیه)
        # time_factor: ضریب سرعت شبیه‌سازی (1.0 = زمان واقعی، 10.0 = ده برابر سریعتر)
        self.dt = 0.1
        self.time_factor = 5.0 

    def add_drone(self, drone):
        """یک پهپاد به شبیه‌سازی اضافه می‌کند."""
        self.drones.append(drone)
        print(f"Drone {drone.id} added to the simulation.")

    def run(self):
        """حلقه اصلی شبیه‌سازی را اجرا می‌کند."""
        if not self.drones:
            print("Simulation Error: No drones to simulate.")
            return

        print("\n--- Starting Simulation ---")
        print(f"Time Step (dt): {self.dt}s | Simulation Speed: {self.time_factor}x")
        
        self.is_running = True
        sim_time = 0.0

        try:
            while self.is_running:
                # به‌روزرسانی وضعیت تمام پهپادها
                for drone in self.drones:
                    drone.update(self.dt)
                    print(drone) # چاپ وضعیت فعلی پهپاد

                # بررسی شرط پایان شبیه‌سازی
                # اگر تمام پهپادها به وضعیت FINISHED رسیده‌اند، حلقه را متوقف کن
                if all(drone.status == drone.status.FINISHED for drone in self.drones):
                    self.is_running = False
                
                # مدیریت زمان
                sim_time += self.dt
                # مکث برای ایجاد حس زمان واقعی (تقسیم بر ضریب سرعت)
                time.sleep(self.dt / self.time_factor)

        except KeyboardInterrupt:
            print("\nSimulation stopped by user.")
        finally:
            print(f"\n--- Simulation Finished ---")
            print(f"Total simulated time: {sim_time:.2f} seconds.")
