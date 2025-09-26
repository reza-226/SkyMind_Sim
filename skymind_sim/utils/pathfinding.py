# skymind_sim/utils/pathfinding.py

import heapq
from typing import List, Tuple

def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """
    محاسبه فاصله منهتن بین دو نقطه. این تابع تخمینی (heuristic)
    از هزینه رسیدن از نقطه a به نقطه b ارائه می‌دهد.
    """
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(
    grid: List[List[str]],
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> List[Tuple[int, int]]:
    """
    الگوریتم مسیریابی A* برای پیدا کردن کوتاه‌ترین مسیر در یک گرید.

    :param grid: نقشه محیط به صورت یک لیست دو بعدی.
    :param start: مختصات نقطه شروع (x, y).
    :param goal: مختصات نقطه هدف (x, y).
    :return: لیستی از مختصات (x, y) که مسیر را از شروع تا هدف نشان می‌دهد.
             اگر مسیری پیدا نشود، لیست خالی برمی‌گرداند.
    """
    rows, cols = len(grid), len(grid[0])
    # همسایه‌های ممکن (بالا، پایین، چپ، راست)
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # صف اولویت برای گره‌هایی که باید بررسی شوند.
    # آیتم‌ها: (هزینه کل تخمینی, هزینه واقعی تا اینجا, مختصات, والد)
    open_list = []
    heapq.heappush(open_list, (0, 0, start, None))

    # برای نگهداری والد هر گره جهت بازسازی مسیر
    came_from = {}
    # برای نگهداری هزینه واقعی رسیدن به هر گره
    g_score = { (r, c): float('inf') for r in range(rows) for c in range(cols) }
    g_score[start] = 0

    while open_list:
        # گره با کمترین هزینه کل تخمینی را از صف بردار
        _, current_g, current_pos, _ = heapq.heappop(open_list)

        if current_pos == goal:
            # مسیر پیدا شد، آن را بازسازی کن
            path = []
            while current_pos in came_from:
                path.append(current_pos)
                current_pos = came_from[current_pos]
            path.append(start)
            return path[::-1] # مسیر را برعکس کن تا از شروع به هدف باشد

        for dr, dc in neighbors:
            neighbor_pos = (current_pos[0] + dr, current_pos[1] + dc)
            r, c = neighbor_pos

            # بررسی اینکه آیا همسایه در محدوده نقشه است و مانع نیست
            if not (0 <= r < rows and 0 <= c < cols and grid[r][c] != 'W'):
                continue

            # هزینه حرکت به این همسایه 1 است
            tentative_g_score = current_g + 1

            if tentative_g_score < g_score[neighbor_pos]:
                # این مسیر به همسایه بهتر از مسیر قبلی است
                came_from[neighbor_pos] = current_pos
                g_score[neighbor_pos] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor_pos, goal)
                heapq.heappush(open_list, (f_score, tentative_g_score, neighbor_pos, current_pos))

    return [] # اگر هیچ مسیری پیدا نشد
