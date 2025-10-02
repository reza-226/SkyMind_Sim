# skymind_sim/layer_3_intelligence/pathfinding/path_planner.py

import logging
from typing import List, Tuple, Optional, Set
from skymind_sim.layer_1_simulation.world.obstacle import Obstacle
from .a_star import a_star_search

logger = logging.getLogger(__name__)

class PathPlanner:
    """
    کلاس مسئول برای پیدا کردن مسیر با استفاده از الگوریتم A*.
    این کلاس دنیای شبیه‌سازی را به یک گرید تبدیل کرده و موانع را برای A* مشخص می‌کند.
    """
    def __init__(self, obstacles: List[Obstacle], world_bounds: Tuple[int, int], grid_size: int = 20):
        """
        :param obstacles: لیستی از تمام اشیاء مانع در شبیه‌سازی.
        :param world_bounds: ابعاد کلی نقشه (width, height).
        :param grid_size: اندازه هر سلول در گرید برای گسسته‌سازی فضا.
        """
        self.world_bounds = world_bounds
        self.grid_size = grid_size
        self.obstacle_grid: Set[Tuple[int, int]] = self._create_obstacle_grid(obstacles)
        logger.info(f"PathPlanner initialized with a grid of size {grid_size}x{grid_size}. "
                    f"{len(self.obstacle_grid)} grid cells are marked as obstacles.")

    def _create_obstacle_grid(self, obstacles: List[Obstacle]) -> Set[Tuple[int, int]]:
        """
        موانع موجود در دنیای شبیه‌سازی را به یک مجموعه از سلول‌های گرید مسدود شده تبدیل می‌کند.
        """
        blocked_cells = set()
        for obs in obstacles:
            # پیدا کردن محدوده گرید که توسط مانع اشغال شده است
            # برای اطمینان از برخورد نکردن، یک حاشیه امن (padding) هم در نظر می‌گیریم
            padding = self.grid_size / 2
            
            start_x = int((obs.rect.left - padding) / self.grid_size)
            end_x = int((obs.rect.right + padding) / self.grid_size)
            start_y = int((obs.rect.top - padding) / self.grid_size)
            end_y = int((obs.rect.bottom + padding) / self.grid_size)

            for x in range(start_x, end_x + 1):
                for y in range(start_y, end_y + 1):
                    blocked_cells.add((x, y))
        
        return blocked_cells

    def find_path(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        مسیر از نقطه شروع به پایان را با استفاده از A* پیدا می‌کند.

        :param start_pos: موقعیت شروع (x, y) در مختصات دنیای واقعی.
        :param end_pos: موقعیت هدف (x, y) در مختصات دنیای واقعی.
        :return: لیستی از نقاط مسیر یا None اگر مسیری پیدا نشود.
        """
        logger.info(f"Finding path from {start_pos} to {end_pos}...")
        
        path = a_star_search(
            start_pos=start_pos,
            end_pos=end_pos,
            obstacles=self.obstacle_grid,
            grid_size=self.grid_size,
            world_bounds=self.world_bounds
        )

        if path:
            logger.info(f"Path found with {len(path)} points.")
            # اینجا می‌توانیم در آینده یک مرحله ساده‌سازی مسیر (path smoothing) اضافه کنیم
            return path
        else:
            logger.warning(f"No path found from {start_pos} to {end_pos}.")
            return None
