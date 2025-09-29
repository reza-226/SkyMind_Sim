# skymind_sim/core/path_planner.py

import numpy as np
from .environment import Environment

class PathPlanner:
    """
    مسئولیت پیدا کردن مسیر برای پهپادها در محیط را بر عهده دارد.
    در این نسخه اولیه، فقط محیط را به یک گرید (شبکه) از موانع تبدیل می‌کند.
    """
    def __init__(self, environment: Environment, grid_resolution=1.0):
        """
        Args:
            environment (Environment): آبجکت محیط شبیه‌سازی.
            grid_resolution (float): اندازه هر سلول در گرید (بر حسب متر).
        """
        if environment is None:
            raise ValueError("Environment object cannot be None.")
            
        self.env = environment
        self.resolution = grid_resolution
        
        # لاگ‌های جدید برای نمایش اطلاعات
        print(f"Environment dimensions: {self.env.dimensions}")
        
        # محاسبه ابعاد گرید
        self.grid_dims = np.ceil(self.env.dimensions / self.resolution).astype(int)
        
        print(f"Grid resolution: {self.resolution}m")
        print(f"Calculated grid dimensions: {self.grid_dims}")
        total_cells = np.prod(self.grid_dims)
        print(f"Total grid cells to process: {total_cells:,}")

        # ایجاد گرید سه بعدی موانع
        self.obstacle_grid = np.zeros(self.grid_dims, dtype=np.uint8)
        
        # ساخت گرید موانع
        self._build_obstacle_grid()

    def _build_obstacle_grid(self):
        """
        گرید موانع را با بررسی مرکز هر سلول گرید پر می‌کند.
        """
        print("Building obstacle grid...")
        if not self.env.obstacles:
            print("No obstacles in the environment. Grid is empty.")
            return

        for i in range(self.grid_dims[0]):
            for j in range(self.grid_dims[1]):
                for k in range(self.grid_dims[2]):
                    # محاسبه مختصات مرکز سلول گرید
                    grid_cell_center = np.array([
                        (i + 0.5) * self.resolution,
                        (j + 0.5) * self.resolution,
                        (k + 0.5) * self.resolution
                    ])
                    
                    # بررسی برخورد با هر مانع
                    for obstacle in self.env.obstacles:
                        if obstacle.is_colliding(grid_cell_center):
                            self.obstacle_grid[i, j, k] = 1
                            break 
        
        print("Obstacle grid built successfully.")

    def find_path(self, start_pos, goal_pos):
        """
        الگوریتم مسیریابی (در آینده پیاده‌سازی می‌شود).
        """
        print(f"Pathfinding from {start_pos} to {goal_pos} is not implemented yet.")
        return None
