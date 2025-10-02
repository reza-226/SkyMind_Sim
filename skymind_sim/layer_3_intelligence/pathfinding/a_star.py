# مسیر: skymind_sim/layer_3_intelligence/pathfinding/a_star.py

import heapq
import numpy as np
import logging

def a_star(grid: np.ndarray, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]] | None:
    """
    الگوریتم A* برای پیدا کردن کوتاه‌ترین مسیر در یک گرید.

    Args:
        grid (np.ndarray): یک آرایه دوبعدی NumPy که نقشه را نشان می‌دهد. 
                           0 برای مسیر قابل عبور و 1 برای مانع.
        start (tuple[int, int]): مختصات نقطه شروع (row, col).
        goal (tuple[int, int]): مختصات نقطه هدف (row, col).

    Returns:
        list[tuple[int, int]] | None: لیستی از تاپل‌های مختصات مسیر از شروع تا هدف،
                                     یا None اگر مسیری پیدا نشود.
    """
    logger = logging.getLogger(__name__)
    rows, cols = grid.shape
    open_set = [(0, start)]  # (f_score, (row, col))
    came_from = {}
    g_score = { (r, c): float('inf') for r in range(rows) for c in range(cols) }
    g_score[start] = 0
    f_score = { (r, c): float('inf') for r in range(rows) for c in range(cols) }
    f_score[start] = _heuristic(start, goal)

    open_set_hash = {start}

    while open_set:
        _, current = heapq.heappop(open_set)
        open_set_hash.remove(current)

        if current == goal:
            return _reconstruct_path(came_from, current)

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]: # 8 جهت حرکت
            neighbor = (current[0] + dr, current[1] + dc)
            
            # بررسی اینکه همسایه داخل محدوده نقشه باشد
            if not (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols):
                continue

            # بررسی اینکه همسایه مانع نباشد
            if grid[neighbor[0], neighbor[1]] == 1:
                continue
            
            # هزینه حرکت از current به neighbor (1 برای حرکات اصلی، sqrt(2) برای حرکات قطری)
            move_cost = 1.414 if dr != 0 and dc != 0 else 1.0
            tentative_g_score = g_score[current] + move_cost

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + _heuristic(neighbor, goal)
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)
    
    logger.warning(f"A* pathfinding failed: No path found from {start} to {goal}.")
    return None # اگر مسیری پیدا نشد

def _heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
    """
    تابع هیوریستیک (فاصله اقلیدسی) برای تخمین فاصله تا هدف.
    """
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def _reconstruct_path(came_from: dict, current: tuple[int, int]) -> list[tuple[int, int]]:
    """
    بازسازی مسیر نهایی از دیکشنری came_from.
    """
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1] # معکوس کردن لیست برای دریافت مسیر از شروع به هدف

# توجه: تابع a_star_numba دیگر وجود ندارد. فقط a_star داریم.
