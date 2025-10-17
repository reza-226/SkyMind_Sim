# FILE: skymind_sim/layer_3_intelligence/pathfinding/a_star.py

import heapq
from typing import List, Tuple, Optional

from skymind_sim.layer_1_simulation.world.grid import Grid, Cell

# === شروع تغییرات ===
# 1. وارد کردن LogManager به جای Logger
from skymind_sim.utils.log_manager import LogManager

# 2. دریافت لاگر با استفاده از LogManager
logger = LogManager.get_logger(__name__)
# === پایان تغییرات ===


class AStarPlanner:
    """
    الگوریتم A* را برای پیدا کردن کوتاه‌ترین مسیر در یک گرید پیاده‌سازی می‌کند.
    """

    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """فاصله منهتن را به عنوان تابع هیوریستیک محاسبه می‌کند."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _reconstruct_path(self, came_from: dict, current: Cell) -> List[Tuple[int, int]]:
        """مسیر نهایی را با دنبال کردن والدین هر گره از انتها به ابتدا بازسازی می‌کند."""
        total_path = [current.position]
        while current in came_from:
            current = came_from[current]
            total_path.insert(0, current.position)
        return total_path

    def find_path(self, grid: Grid, start: Tuple[int, int], end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        کوتاه‌ترین مسیر بین دو نقطه را با استفاده از A* پیدا می‌کند.

        Args:
            grid (Grid): گرید شبیه‌سازی که شامل موانع است.
            start (Tuple[int, int]): مختصات گرید نقطه شروع.
            end (Tuple[int, int]): مختصات گرید نقطه پایان.

        Returns:
            Optional[List[Tuple[int, int]]]: لیستی از مختصات گرید که مسیر را تشکیل می‌دهند، یا None اگر مسیری پیدا نشود.
        """
        logger.debug(f"A* pathfinding started from {start} to {end}.")
        grid.reset_pathfinding_data()

        start_cell = grid.get_cell(start[0], start[1])
        end_cell = grid.get_cell(end[0], end[1])

        if not start_cell or not end_cell or start_cell.is_obstacle or end_cell.is_obstacle:
            logger.warning("Start or end cell is invalid or an obstacle.")
            return None

        open_set = []
        heapq.heappush(open_set, (0, start_cell)) # (f_score, cell)

        came_from = {}
        start_cell.g_score = 0
        start_cell.f_score = self._heuristic(start, end)

        open_set_hash = {start_cell}

        while open_set:
            current_cell: Cell = heapq.heappop(open_set)[1]
            open_set_hash.remove(current_cell)

            if current_cell == end_cell:
                logger.info(f"Path found from {start} to {end}.")
                return self._reconstruct_path(came_from, current_cell)

            for neighbor_cell in grid.get_neighbors(current_cell):
                tentative_g_score = current_cell.g_score + 1  # Cost to move is 1

                if tentative_g_score < neighbor_cell.g_score:
                    came_from[neighbor_cell] = current_cell
                    neighbor_cell.g_score = tentative_g_score
                    neighbor_cell.f_score = tentative_g_score + self._heuristic(neighbor_cell.position, end)
                    if neighbor_cell not in open_set_hash:
                        heapq.heappush(open_set, (neighbor_cell.f_score, neighbor_cell))
                        open_set_hash.add(neighbor_cell)
        
        logger.warning(f"No path could be found from {start} to {end}.")
        return None
