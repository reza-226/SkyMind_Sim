# skymind_sim/core/path_planner.py

import numpy as np
import heapq
from typing import List, Tuple, Optional, Set

class PathPlanner:
    """
    کلاسی برای یافتن مسیر در یک محیط گسسته‌سازی شده با استفاده از الگوریتم A*.
    """

    def __init__(self, environment, grid_resolution: float = 1.0):
        """
        سازنده کلاس PathPlanner.

        Args:
            environment: نمونه‌ای از کلاس Environment که شامل موانع است.
            grid_resolution (float): اندازه هر سلول در شبکه گسسته‌سازی شده.
        """
        self.environment = environment
        self.grid_resolution = grid_resolution
        self._obstacle_grid: Optional[Set[Tuple[int, int, int]]] = None
        self._build_obstacle_grid()

    def _world_to_grid(self, world_coords: np.ndarray) -> Tuple[int, int, int]:
        """مختصات دنیای واقعی را به مختصات شبکه تبدیل می‌کند."""
        return tuple(np.floor(world_coords / self.grid_resolution).astype(int))

    def _grid_to_world(self, grid_coords: Tuple[int, int, int]) -> np.ndarray:
        """مختصات شبکه را به مرکز سلول در دنیای واقعی تبدیل می‌کند."""
        return (np.array(grid_coords) + 0.5) * self.grid_resolution

    def _build_obstacle_grid(self):
        """
        یک شبکه گسسته از موانع ایجاد می‌کند تا بررسی برخورد سریع‌تر انجام شود.
        این تابع یک بار در هنگام مقداردهی اولیه اجرا می‌شود.
        """
        self._obstacle_grid = set()
        if not self.environment.obstacles:
            return

        dims = self.environment.dimensions
        # محاسبه مرزهای شبکه
        min_grid = self._world_to_grid(np.array([0, 0, 0]))
        max_grid = self._world_to_grid(dims)

        for x in range(min_grid[0], max_grid[0] + 1):
            for y in range(min_grid[1], max_grid[1] + 1):
                for z in range(min_grid[2], max_grid[2] + 1):
                    grid_cell_center = self._grid_to_world((x, y, z))
                    # بررسی می‌کنیم آیا مرکز سلول شبکه داخل هیچ مانعی قرار دارد یا خیر
                    for obstacle in self.environment.obstacles:
                        if obstacle.is_inside(grid_cell_center):
                            self._obstacle_grid.add((x, y, z))
                            break # اگر داخل یک مانع بود، نیازی به بررسی بقیه نیست

    def _is_valid_grid_cell(self, grid_coords: Tuple[int, int, int]) -> bool:
        """بررسی می‌کند که آیا یک سلول شبکه معتبر است (داخل مانع نیست)."""
        return grid_coords not in self._obstacle_grid

    def _get_neighbors(self, grid_coords: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        """همسایه‌های یک سلول در شبکه را برمی‌گرداند."""
        x, y, z = grid_coords
        neighbors = []
        # بررسی 26 همسایه ممکن در یک شبکه سه‌بعدی
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == 0 and dy == 0 and dz == 0:
                        continue
                    neighbor = (x + dx, y + dy, z + dz)
                    neighbors.append(neighbor)
        return neighbors

    def _heuristic(self, a: Tuple[int, int, int], b: Tuple[int, int, int]) -> float:
        """تابع هیوریستیک (فاصله اقلیدسی) بین دو نقطه در شبکه را محاسبه می‌کند."""
        return np.linalg.norm(np.array(a) - np.array(b))

    def find_path(self, start_pos: np.ndarray, goal_pos: np.ndarray) -> Optional[List[np.ndarray]]:
        """
        یک مسیر از نقطه شروع به هدف با استفاده از الگوریتم A* پیدا می‌کند.

        Args:
            start_pos (np.ndarray): مختصات نقطه شروع در دنیای واقعی.
            goal_pos (np.ndarray): مختصات نقطه هدف در دنیای واقعی.

        Returns:
            Optional[List[np.ndarray]]: لیستی از نقاط مسیر در دنیای واقعی یا None اگر مسیری پیدا نشود.
        """
        start_grid = self._world_to_grid(start_pos)
        goal_grid = self._world_to_grid(goal_pos)

        if not self._is_valid_grid_cell(start_grid) or not self._is_valid_grid_cell(goal_grid):
            print("Warning: Start or goal is inside an obstacle.")
            return None

        open_set = [(0, start_grid)]  # (f_score, node)
        heapq.heapify(open_set)
        
        came_from = {}
        g_score = {start_grid: 0}
        f_score = {start_grid: self._heuristic(start_grid, goal_grid)}

        while open_set:
            _, current_grid = heapq.heappop(open_set)

            if current_grid == goal_grid:
                return self._reconstruct_path(came_from, current_grid)

            for neighbor_grid in self._get_neighbors(current_grid):
                if not self._is_valid_grid_cell(neighbor_grid):
                    continue

                # هزینه حرکت از current به neighbor (1 برای حرکات مستقیم، sqrt(2) برای قطری، sqrt(3) برای قطری سه‌بعدی)
                tentative_g_score = g_score[current_grid] + self._heuristic(current_grid, neighbor_grid)

                if tentative_g_score < g_score.get(neighbor_grid, float('inf')):
                    came_from[neighbor_grid] = current_grid
                    g_score[neighbor_grid] = tentative_g_score
                    f_score[neighbor_grid] = tentative_g_score + self._heuristic(neighbor_grid, goal_grid)
                    heapq.heappush(open_set, (f_score[neighbor_grid], neighbor_grid))

        print("Path not found!")
        return None

    def _reconstruct_path(self, came_from: dict, current_grid: Tuple[int, int, int]) -> List[np.ndarray]:
        """مسیر نهایی را از دیکشنری came_from بازسازی می‌کند."""
        total_path = [self._grid_to_world(current_grid)]
        while current_grid in came_from:
            current_grid = came_from[current_grid]
            total_path.append(self._grid_to_world(current_grid))
        return total_path[::-1]  # مسیر را برعکس می‌کنیم تا از شروع به پایان باشد
