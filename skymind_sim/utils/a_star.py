# skymind_sim/utils/a_star.py

import heapq
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..core.environment import Environment

def manhattan_distance(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
    """
    محاسبه فاصله منهتن بین دو نقطه.
    h(n) در الگوریتم A*.
    """
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(env: 'Environment', start: tuple[int, int], end: tuple[int, int]) -> Optional[list[tuple[int, int]]]:
    """
    الگوریتم A* برای پیدا کردن کوتاه‌ترین مسیر در محیط.
    
    :param env: شیء محیط که نقشه و موانع را در خود دارد.
    :param start: مختصات نقطه شروع (x, y).
    :param end: مختصات نقطه پایان (x, y).
    :return: لیستی از مختصات مسیر از شروع تا پایان، یا None اگر مسیری پیدا نشود.
    """
    # صف اولویت برای گره‌هایی که باید بررسی شوند.
    # آیتم‌ها به صورت (هزینه_f, مختصات) ذخیره می‌شوند.
    open_set = [(0, start)]
    heapq.heapify(open_set)

    # دیکشنری برای نگهداری گره قبلی در بهترین مسیر پیدا شده تا کنون
    came_from: dict[tuple[int, int], tuple[int, int]] = {}

    # هزینه مسیر از شروع تا هر گره (g_score)
    g_score: dict[tuple[int, int], float] = {start: 0}

    # هزینه کل تخمینی از شروع تا پایان از طریق هر گره (f_score)
    # f_score = g_score + heuristic
    f_score: dict[tuple[int, int], float] = {start: manhattan_distance(start, end)}

    while open_set:
        # گره با کمترین f_score را از صف اولویت بردار
        _, current = heapq.heappop(open_set)

        # اگر به مقصد رسیدیم، مسیر را بازسازی کن
        if current == end:
            return reconstruct_path(came_from, current)

        # همسایه‌های معتبر گره فعلی را بررسی کن
        for neighbor in env.get_neighbors(current):
            # هزینه حرکت به همسایه همیشه 1 است (در شبکه ما)
            tentative_g_score = g_score[current] + 1
            
            # اگر این مسیر به همسایه بهتر از مسیرهای قبلی است
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                # این مسیر جدید به همسایه را ثبت کن
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, end)
                
                # اگر همسایه در صف اولویت نبود، آن را اضافه کن
                if (f_score[neighbor], neighbor) not in open_set:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # اگر حلقه تمام شد و به مقصد نرسیدیم، یعنی مسیری وجود ندارد
    return None


def reconstruct_path(came_from: dict[tuple[int, int], tuple[int, int]], current: tuple[int, int]) -> list[tuple[int, int]]:
    """
    مسیر را از آخر به اول بازسازی می‌کند.
    """
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    
    # مسیر را برعکس کن تا از شروع به پایان باشد
    return total_path[::-1]
