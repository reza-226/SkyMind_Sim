# skymind_sim/core/environment.py

import json
import numpy as np
# ایمپورت را به بالای فایل منتقل می‌کنیم، چون از خطای circular import جلوگیری کرده‌ایم
from .obstacle import BoxObstacle 

class Environment:
    """
    محیط شبیه‌سازی را مدیریت می‌کند، شامل ابعاد، موانع و گرید اشغال.
    """
    def __init__(self):
        """سازنده ساده که مقادیر اولیه را None قرار می‌دهد تا بعداً از فایل بارگذاری شوند."""
        self.dimensions = None
        self.grid_resolution = None
        self.obstacles = []
        self.start_point = None
        self.end_point = None
        self.grid = None
        self.grid_dim = None

    def load_from_json(self, file_path):
        """
        یک نقشه محیط را از فایل JSON بارگذاری و تمام مشخصات محیط را مقداردهی اولیه می‌کند.
        """
        try:
            print(f"Loading map from '{file_path}'...")
            with open(file_path, 'r') as f:
                data = json.load(f)

            # بارگذاری ابعاد محیط و رزولوشن گرید
            env_data = data['environment']
            self.dimensions = np.array(env_data['dimensions'], dtype=float)
            self.grid_resolution = float(env_data.get('grid_resolution', 1.0)) # استفاده از مقدار پیش‌فرض
            self.grid_dim = np.ceil(self.dimensions / self.grid_resolution).astype(int)
            
            print(f"Environment dimensions: {self.dimensions}")
            print(f"Grid resolution: {self.grid_resolution}m")
            print(f"Calculated grid dimensions: {self.grid_dim}")
            total_cells = np.prod(self.grid_dim)
            print(f"Total grid cells to process: {total_cells}")

            # بارگذاری موانع
            self.obstacles = []
            if 'obstacles' in data:
                for obs_data in data['obstacles']:
                    if obs_data.get('type') == 'box':
                        # راه حل مشکل 2: استفاده از from_dict که انعطاف‌پذیر است
                        self.obstacles.append(BoxObstacle.from_dict(obs_data))
            
            # بارگذاری نقاط شروع و پایان
            self.start_point = np.array(data['start_point'], dtype=float)
            self.end_point = np.array(data['end_point'], dtype=float)

            # ساخت گرید اشغال بر اساس موانع بارگذاری شده
            self._build_obstacle_grid()

            print("Environment loaded successfully.")
            return True

        except (FileNotFoundError, KeyError, ValueError) as e:
            print(f"An unexpected error occurred while loading the map: {e}")
            return False

    def _build_obstacle_grid(self):
        """
        یک گرید سه‌بعدی می‌سازد و سلول‌هایی که توسط موانع اشغال شده‌اند را علامت‌گذاری می‌کند.
        این نسخه به جای محاسبه bounding box، مرکز هر سلول را چک می‌کند که دقیق‌تر است.
        """
        print("Building obstacle grid...")
        self.grid = np.zeros(self.grid_dim, dtype=np.uint8)

        # محاسبه مختصات مرکز هر سلول گرید یک بار
        x_coords = np.arange(self.grid_dim[0]) * self.grid_resolution + self.grid_resolution / 2
        y_coords = np.arange(self.grid_dim[1]) * self.grid_resolution + self.grid_resolution / 2
        z_coords = np.arange(self.grid_dim[2]) * self.grid_resolution + self.grid_resolution / 2
        
        # تکرار روی هر مانع و علامت‌گذاری سلول‌های مربوطه
        for obs in self.obstacles:
            # راه حل مشکل 1: استفاده از obs.center به جای obs.position
            min_bound = obs.center - (obs.size / 2)
            max_bound = obs.center + (obs.size / 2)
            
            # تبدیل گوشه‌های مانع به اندیس‌های گرید
            min_grid_idx = np.floor(min_bound / self.grid_resolution).astype(int)
            max_grid_idx = np.ceil(max_bound / self.grid_resolution).astype(int)

            # محدود کردن به ابعاد گرید برای جلوگیری از خطا
            min_grid_idx = np.maximum(min_grid_idx, 0)
            max_grid_idx = np.minimum(max_grid_idx, self.grid_dim)
            
            # پر کردن بخش مربوط به مانع در گرید
            self.grid[min_grid_idx[0]:max_grid_idx[0], 
                      min_grid_idx[1]:max_grid_idx[1], 
                      min_grid_idx[2]:max_grid_idx[2]] = 1

        print("Obstacle grid built successfully.")

    def world_to_grid(self, world_coords):
        """مختصات دنیای واقعی را به اندیس گرید تبدیل می‌کند."""
        grid_coords = np.floor(np.array(world_coords) / self.grid_resolution).astype(int)
        return np.clip(grid_coords, 0, self.grid_dim - 1)

    def grid_to_world(self, grid_coords):
        """اندیس گرید را به مرکز مختصات دنیای واقعی آن سلول تبدیل می‌کند."""
        return (np.array(grid_coords) * self.grid_resolution) + (self.grid_resolution / 2.0)

    def is_obstacle(self, grid_coords):
        """بررسی می‌کند که آیا یک سلول گرید مانع است یا خیر."""
        i, j, k = grid_coords
        # بررسی مرزها
        if not (0 <= i < self.grid_dim[0] and 0 <= j < self.grid_dim[1] and 0 <= k < self.grid_dim[2]):
            return True # خارج از مرزها مانع است
        return self.grid[i, j, k] == 1

