# skymind_sim/core/environment.py

from typing import Tuple, Set, List
from .drone import Drone

# تعریف نوع برای مختصات برای خوانایی بهتر
Position = Tuple[int, int]

class Environment:
    """
    نماینده دنیای شبیه‌سازی، شامل نقشه، موانع و پهپادها.
    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.obstacles: Set[Position] = set()
        self.drones: List[Drone] = []
        # دیکشنری برای نگهداری موقعیت پهپادها و شناسه آن‌ها
        # به ما اجازه می‌دهد چند پهپاد در یک نقطه داشته باشیم
        self.drone_locations: dict[Position, Set[str]] = {}

    def is_valid_position(self, pos: Position) -> bool:
        """بررسی می‌کند که آیا یک موقعیت در محدوده نقشه است یا خیر."""
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def add_obstacle(self, pos: Position):
        """یک مانع را به محیط اضافه می‌کند."""
        if self.is_valid_position(pos):
            self.obstacles.add(pos)
            print(f"[Environment] Added obstacle at {pos}.")
        else:
            print(f"[Warning] Obstacle position {pos} is out of bounds.")

    def add_drone(self, drone: Drone) -> bool:
        """یک پهپاد را به محیط اضافه می‌کند."""
        pos = drone.position
        if not self.is_valid_position(pos):
            print(f"[Error] Drone start position {pos} is out of bounds.")
            return False
        if pos in self.obstacles:
            print(f"[Error] Cannot place drone at {pos}, an obstacle is present.")
            return False
        
        # استفاده از drone.drone_id به جای drone.id
        print(f"[Environment] Adding drone '{drone.drone_id}' at {drone.position}.")
        self.drones.append(drone)
        
        if pos not in self.drone_locations:
            self.drone_locations[pos] = set()
        
        # استفاده از drone.drone_id به جای drone.id
        self.drone_locations[pos].add(drone.drone_id)
        return True

    def update_drone_position(self, drone: Drone):
        """
        موقعیت یک پهپاد خاص را روی نقشه داخلی محیط به‌روز می‌کند.
        این تابع فرض می‌کند که موقعیت جدید معتبر است.
        """
        drone_id_to_remove = drone.drone_id
        # ابتدا موقعیت قبلی پهپاد را از دیکشنری پاک می‌کنیم
        for pos, drone_ids in list(self.drone_locations.items()):
            if drone_id_to_remove in drone_ids:
                drone_ids.remove(drone_id_to_remove)
                if not drone_ids: # اگر این آخرین پهپاد در این نقطه بود، کلید را پاک کن
                    del self.drone_locations[pos]
                break # چون هر پهپاد فقط در یک مکان است، پس از یافتن، حلقه را می‌شکنیم
        
        # افزودن پهپاد به موقعیت جدیدش
        new_pos = drone.position
        if new_pos not in self.drone_locations:
            self.drone_locations[new_pos] = set()
        self.drone_locations[new_pos].add(drone.drone_id)

    def display(self):
        """محیط را در ترمینال نمایش می‌دهد."""
        print("\n" + "="*20 + " Environment Map " + "="*20)
        # ایجاد یک گرید خالی
        grid = [['.' for _ in range(self.width)] for _ in range(self.height)]

        # قرار دادن موانع در گرید
        for obs_pos in self.obstacles:
            x, y = obs_pos
            if self.is_valid_position(obs_pos):
                grid[y][x] = 'X'
        
        # قرار دادن پهپادها در گرید
        for drone_pos, drone_ids in self.drone_locations.items():
            x, y = drone_pos
            if self.is_valid_position(drone_pos):
                # اگر بیش از یک پهپاد در یک نقطه بود، عدد نمایش بده
                display_char = 'D' if len(drone_ids) == 1 else str(len(drone_ids))
                grid[y][x] = display_char

        # چاپ گرید به همراه محورها
        # چاپ از بالا به پایین (y از height-1 تا 0) تا مبدا مختصات پایین-چپ باشد
        for y in range(self.height - 1, -1, -1):
            row_str = " ".join(grid[y])
            print(f"{y:2d}| {row_str}")
        
        print("  +" + "-" * (self.width * 2 - 1))
        print("   " + " ".join([f"{x:<1d}" for x in range(self.width)]))
        print("="*57 + "\n")
