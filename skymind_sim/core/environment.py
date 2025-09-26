# skymind_sim/core/environment.py

import numpy as np
from typing import Tuple, List, Optional
from .drone import Drone

class Environment:
    """
    کلاسی برای نمایش و مدیریت محیط شبیه‌سازی (نقشه).
    """
    def __init__(self, map_file_path: str):
        """
        سازنده کلاس محیط.
        """
        self.grid, self.start_pos, self.end_pos = self._load_map(map_file_path)
        if self.grid is None:
            raise ValueError(f"Map file could not be loaded or is invalid: {map_file_path}")
        
        self.height, self.width = self.grid.shape
        self.drones: List[Drone] = []
        print(f"Environment loaded from '{map_file_path}' ({self.width}x{self.height}).")
        print(f"Start: {self.start_pos}, End: {self.end_pos}")

# در فایل skymind_sim/core/environment.py

    def _load_map(self, file_path: str) -> Tuple[Optional[np.ndarray], Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
        """
        نقشه را از یک فایل متنی بارگذاری می‌کند، خطوط خالی را نادیده می‌گیرد
        و کاراکترهای خاص را مدیریت می‌کند.
        """
        try:
            processed_lines = []
            with open(file_path, 'r') as f:
                for line in f:
                    stripped_line = line.rstrip('\n')
                    if not stripped_line:
                        continue # نادیده گرفتن خطوط خالی

                    # جایگزینی کاراکتر '.' با فضای خالی ' ' برای مسیریابی
                    processed_line = list(stripped_line.replace('.', ' '))
                    processed_lines.append(processed_line)
            
            if not processed_lines:
                print("Error loading map: Map file is empty or contains only whitespace.")
                return None, None, None

            # بررسی یکسان بودن طول خطوط
            first_line_len = len(processed_lines[0])
            if not all(len(line) == first_line_len for line in processed_lines):
                 print("Error loading map: Not all lines have the same length.")
                 # برای دیباگ کردن بهتر، طول خطوط نابرابر را چاپ می‌کنیم
                 for i, line in enumerate(processed_lines):
                     if len(line) != first_line_len:
                         print(f"  -> Line {i+1} has length {len(line)}, expected {first_line_len}.")
                 return None, None, None

            grid = np.array(processed_lines)
            start_pos, end_pos = None, None
            
            # پیدا کردن S و E در گرید نهایی
            start_coords = np.where(grid == 'S')
            end_coords = np.where(grid == 'E')

            if start_coords[0].size > 0:
                start_pos = (start_coords[0][0], start_coords[1][0])
            if end_coords[0].size > 0:
                end_pos = (end_coords[0][0], end_coords[1][0])
            
            if start_pos is None or end_pos is None:
                print("Error loading map: Start 'S' or End 'E' position not found in map.")
                return None, None, None

            return grid, start_pos, end_pos
        except FileNotFoundError:
            print(f"Error: Map file not found at '{file_path}'")
            return None, None, None
        except Exception as e:
            print(f"An unexpected error occurred while loading the map: {e}")
            return None, None, None


    def add_drone(self, drone: Drone):
        """
        یک پهپاد به محیط اضافه می‌کند.
        """
        self.drones.append(drone)
        drone.set_environment(self)

    def is_obstacle(self, position: Tuple[int, int]) -> bool:
        """
        بررسی می‌کند که آیا یک موقعیت مانع است یا خیر.
        """
        r, c = position
        if not (0 <= r < self.height and 0 <= c < self.width):
            return True # خارج از محدوده نقشه به عنوان مانع در نظر گرفته می‌شود
        return self.grid[r, c] == '#'

    def get_display_grid(self) -> np.ndarray:
        """
        یک کپی از گرید نمایشی را برای استفاده در شبیه‌ساز برمی‌گرداند.
        """
        display_grid = np.copy(self.grid)
        
        for drone in self.drones:
            if drone.is_active:
                r, c = drone.position
                # فقط در صورتی کاراکتر پهپاد را جایگزین کن که نقطه شروع یا پایان نباشد
                if display_grid[r, c] not in ('S', 'E'):
                    display_grid[r, c] = 'D'
        
        return display_grid
