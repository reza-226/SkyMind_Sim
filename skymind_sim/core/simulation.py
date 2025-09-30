# skymind_sim/core/simulation.py

import time
from .drone import Drone
from .environment import Environment

class Simulation:
    """
    کلاس اصلی برای مدیریت و اجرای شبیه‌سازی.
    """
    def __init__(self, environment: Environment, drone: Drone):
        """
        سازنده کلاس Simulation.

        Args:
            environment (Environment): شیء محیط شبیه‌سازی.
            drone (Drone): شیء پهپادی که در شبیه‌سازی شرکت می‌کند.
        """
        self.environment = environment
        self.drone = drone
        self.is_running = False
        print("Simulation initialized.")

    def _display_state(self, path: list):
        """
        یک نمایش ساده متنی از وضعیت شبیه‌سازی را در ترمینال چاپ می‌کند.
        """
        # پاک کردن صفحه ترمینال برای ایجاد انیمیشن ساده
        print("\033c", end="") # این کد برای پاک کردن ترمینال در سیستم‌های سازگار با ANSI است

        drone_pos = self.drone.position
        start_pos = path[0]
        end_pos = path[-1]

        print("--- SkyMind Simulation ---")
        print(f"Time: {time.strftime('%H:%M:%S')}")
        print("-" * 26)
        print(f"Drone Status: {self.drone.status}")
        print(f"Drone Position: ({drone_pos[0]:.0f}, {drone_pos[1]:.0f}, {drone_pos[2]:.0f})")
        print(f"Drone Battery: {self.drone.battery:.1f}%")
        print("-" * 26)
        print(f"Path Start: {start_pos}")
        print(f"Path End:   {end_pos}")
        print(f"Path Waypoints: {len(path)}")
        print("\nVisual Representation (Top-Down View):")

        # ایجاد یک نمایش ساده 2D از نقشه
        width = 40  # عرض نمایش
        height = 20 # ارتفاع نمایش
        
        # تبدیل مختصات جهان واقعی به مختصات نمایشگر کوچک
        map_width, map_height, _ = self.environment.dimensions
        
        def to_grid(pos):
            gx = int(pos[0] * width / map_width)
            gy = int(pos[1] * height / map_height)
            return gx, gy

        grid = [['.' for _ in range(width)] for _ in range(height)]

        # نمایش موانع
        for obs_point in self.environment.obstacles:
            ox, oy = to_grid(obs_point)
            if 0 <= oy < height and 0 <= ox < width:
                grid[oy][ox] = '#'
        
        # نمایش مسیر
        for point in path:
            px, py = to_grid(point)
            if 0 <= py < height and 0 <= px < width and grid[py][px] == '.':
                 grid[py][px] = '*'
        
        # نمایش پهپاد
        dx, dy = to_grid(drone_pos)
        if 0 <= dy < height and 0 <= dx < width:
            grid[dy][dx] = 'D'

        # چاپ گرید
        for row in grid:
            print(" ".join(row))

    def run(self, path: list, simulation_speed: float = 0.1):
        """
        حلقه اصلی شبیه‌سازی را اجرا می‌کند.

        Args:
            path (list): لیستی از نقاط (waypoints) که پهپاد باید طی کند.
            simulation_speed (float): تأخیر بین هر گام شبیه‌سازی (به ثانیه).
        """
        if not path:
            print("Simulation cannot run: No path provided.")
            return

        print("\n--- Starting Simulation Run ---")
        self.is_running = True
        
        # حلقه روی تمام نقاط مسیر (به جز نقطه شروع که پهپاد از قبل آنجاست)
        for i, waypoint in enumerate(path[1:]):
            if not self.is_running:
                print("Simulation stopped.")
                break
                
            # پهپاد را به نقطه بعدی در مسیر منتقل کن
            self.drone.move_to(waypoint)
            
            # نمایش وضعیت فعلی در ترمینال
            self._display_state(path)
            
            print(f"\nStep {i+1}/{len(path)-1}: Moving to {waypoint}")

            # تأخیر برای قابل مشاهده کردن شبیه‌سازی
            time.sleep(simulation_speed)
        
        self.is_running = False
        self.drone.status = 'LANDED'
        self._display_state(path) # نمایش وضعیت نهایی
        print("\n--- Simulation Finished ---")
        print(f"Drone reached destination: {self.drone.position}")

    def stop(self):
        """
        شبیه‌سازی را متوقف می‌کند.
        """
        self.is_running = False
