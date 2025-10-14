# مسیر فایل: skymind_sim/layer_3_intelligence/pathfinding/path_planner.py

import logging
from typing import List, Tuple

# ایمپورت صحیح کلاس AStarPlanner
from skymind_sim.layer_3_intelligence.pathfinding.a_star import AStarPlanner
# ایمپورت کلاس Grid برای Type Hinting و بررسی نوع
from skymind_sim.layer_1_simulation.world.grid import Grid

class PathPlanner:
    def __init__(self, grid: Grid):
        self.logger = logging.getLogger(__name__)
        
        if not isinstance(grid, Grid):
            raise TypeError(f"PathPlanner expects a Grid object, but got {type(grid)}")
        
        self.astar_planner = AStarPlanner(grid)
        self.logger.info("PathPlanner initialized with AStarPlanner.")

    def find_path(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        self.logger.info(f"Attempting to find path from {start_pos} to {end_pos}")
        
        # فرض بر اینکه متد در A*، `plan_path` نام دارد
        path = self.astar_planner.plan_path(start_pos, end_pos) 

        if path:
            self.logger.info(f"Path found with {len(path)} steps.")
        else:
            self.logger.warning(f"No path found from {start_pos} to {end_pos}.")
            
        return path
