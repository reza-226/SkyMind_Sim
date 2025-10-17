# FILE: skymind_sim/layer_3_intelligence/pathfinding/path_planner.py

from typing import Optional, List, Tuple
from skymind_sim.layer_1_simulation.world.grid import Grid
from .a_star import AStarPlanner

# === شروع تغییرات ===
# 1. وارد کردن LogManager به جای Logger
from skymind_sim.utils.log_manager import LogManager

# 2. دریافت لاگر با استفاده از LogManager
logger = LogManager.get_logger(__name__)
# === پایان تغییرات ===

class PathPlanner:
    """
    کلاسی برای مدیریت و انتخاب الگوریتم‌های مسیریابی.
    این کلاس به عنوان یک facade عمل می‌کند تا بتوان به راحتی الگوریتم مسیریابی را تغییر داد.
    """
    def __init__(self, algorithm: str = "A_STAR"):
        """
        یک الگوریتم مسیریابی را بر اساس نام آن مقداردهی اولیه می‌کند.
        
        Args:
            algorithm (str): نام الگوریتم مسیریابی (مثلاً "A_STAR").
        """
        self._planner = None
        if algorithm.upper() == "A_STAR":
            self._planner = AStarPlanner()
            logger.info("A* pathfinding algorithm selected.")
        else:
            # در آینده می‌توان الگوریتم‌های دیگری مثل Dijkstra, D*, ... را اضافه کرد.
            error_msg = f"Algorithm '{algorithm}' is not supported."
            logger.error(error_msg)
            raise ValueError(error_msg)

    def plan_path(self, grid: Grid, start: Tuple[int, int], end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        یک مسیر را با استفاده از الگوریتم انتخاب شده برنامه‌ریزی می‌کند.

        Args:
            grid (Grid): گرید شبیه‌سازی.
            start (Tuple[int, int]): نقطه شروع (مختصات گرید).
            end (Tuple[int, int]): نقطه پایان (مختصات گرید).

        Returns:
            Optional[List[Tuple[int, int]]]: لیستی از نقاط مسیر یا None در صورت عدم موفقیت.
        """
        if not self._planner:
            logger.error("No pathfinding algorithm has been initialized.")
            return None
        
        logger.debug(f"PathPlanner delegating path planning from {start} to {end} to the selected algorithm.")
        return self._planner.find_path(grid, start, end)
