from skymind_sim.layer_3_intelligence.pathfinding.a_star import safe_a_star_search
import random

class PathPlanner:
    def __init__(self, grid_map, obstacles=None):
        self.grid_map = grid_map
        self.obstacles = obstacles or []

    def _find_free_goal(self, start):
        """
        پیدا کردن یک سلول آزاد.
        """
        rows, cols = self.grid_map.shape
        free_cells = [
            (x, y)
            for y in range(rows)
            for x in range(cols)
            if (x, y) not in self.obstacles and (x, y) != start
        ]
        random.shuffle(free_cells)
        return free_cells[0] if free_cells else start

    def plan_path(self, start, goal):
        """
        مسیرسازی امن با استفاده از safe_a_star_search.
        """
        path = safe_a_star_search(self.grid_map, start, goal, obstacles=self.obstacles)
        if not path or path == [start]:
            alt_goal = self._find_free_goal(start)
            path = safe_a_star_search(self.grid_map, start, alt_goal, obstacles=self.obstacles)
        return path
