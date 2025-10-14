# FILE: skymind_sim/layer_3_intelligence/pathfinding/a_star.py

import heapq
import logging
from typing import List, Tuple

# ایمپورت‌های جدید برای سازگاری با ساختار شما
from skymind_sim.layer_1_simulation.world.grid import Grid, Cell

logger = logging.getLogger(__name__)

class Node:
    """
    کلاس کمکی برای A*. یک Cell را در خود نگه می‌دارد و هزینه‌های f, g, h را محاسبه می‌کند.
    """
    def __init__(self, parent=None, cell: Cell = None):
        self.parent = parent
        self.cell = cell

        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic cost from current node to end
        self.f = 0  # Total cost (f = g + h)

    def __eq__(self, other):
        return self.cell == other.cell

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        # از مختصات سلول برای نمایش استفاده می‌کنیم
        return f"Node(pos=({self.cell.x}, {self.cell.y}), f={self.f})"


class AStarPlanner:
    """
    مسیریاب A* که با کلاس‌های Grid و Cell جدید شما کار می‌کند.
    """
    def __init__(self, grid: Grid):
        if not isinstance(grid, Grid):
            raise TypeError(f"AStarPlanner expects a Grid object, but got {type(grid)}")
        self.grid = grid
        logger.info(f"AStarPlanner initialized with a grid of size ({self.grid.width}, {self.grid.height})")

    def plan_path(self, start_coords: Tuple[int, int], end_coords: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        محاسبه کوتاه‌ترین مسیر بین دو مختصات.
        """
        logger.debug(f"Planning path from {start_coords} to {end_coords}")

        # گرفتن اشیاء Cell از روی مختصات
        start_cell = self.grid.get_cell(start_coords[0], start_coords[1])
        end_cell = self.grid.get_cell(end_coords[0], end_coords[1])

        if not start_cell or start_cell.is_obstacle:
            logger.warning(f"Start position {start_coords} is invalid or an obstacle.")
            return []
        if not end_cell or end_cell.is_obstacle:
            logger.warning(f"End position {end_coords} is invalid or an obstacle.")
            return []
            
        start_node = Node(None, start_cell)
        end_node = Node(None, end_cell)

        open_list = []
        closed_set = set()
        heapq.heappush(open_list, start_node)

        while open_list:
            current_node = heapq.heappop(open_list)
            closed_set.add(current_node.cell)

            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    # مختصات سلول را به مسیر اضافه می‌کنیم
                    path.append((current.cell.x, current.cell.y))
                    current = current.parent
                logger.info(f"Path found from {start_coords} to {end_coords}.")
                return path[::-1]

            # **استفاده از متد قدرتمند get_neighbors از کلاس Grid شما**
            neighbors = self.grid.get_neighbors(current_node.cell)
            
            for neighbor_cell in neighbors:
                if neighbor_cell in closed_set:
                    continue
                
                # ساخت گره جدید برای همسایه
                child_node = Node(current_node, neighbor_cell)

                # محاسبه هزینه‌ها
                move_cost = 1.4 if child_node.cell.x != current_node.cell.x and child_node.cell.y != current_node.cell.y else 1
                child_node.g = current_node.g + move_cost
                child_node.h = ((child_node.cell.x - end_node.cell.x) ** 2) + ((child_node.cell.y - end_node.cell.y) ** 2)
                child_node.f = child_node.g + child_node.h

                if any(open_node for open_node in open_list if child_node == open_node and child_node.g >= open_node.g):
                    continue

                heapq.heappush(open_list, child_node)

        logger.warning(f"No path found from {start_coords} to {end_coords}.")
        return []
