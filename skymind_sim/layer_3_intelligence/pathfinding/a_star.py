# skymind_sim/layer_3_intelligence/pathfinding/a_star.py

import heapq
import math
from typing import List, Tuple, Optional, Set

# تعریف Node برای استفاده در الگوریتم
class Node:
    """
    یک گره در گراف جستجوی A*.
    حاوی موقعیت، گره والد و هزینه‌های g، h و f.
    """
    def __init__(self, position: Tuple[int, int], parent: Optional['Node'] = None):
        self.position = position
        self.parent = parent
        
        self.g = 0  # هزینه از گره شروع تا گره فعلی
        self.h = 0  # هزینه تخمینی (Heuristic) از گره فعلی تا گره هدف
        self.f = 0  # هزینه کل (f = g + h)

    def __eq__(self, other):
        # دو گره برابرند اگر موقعیت آنها یکی باشد
        return self.position == other.position
    
    def __lt__(self, other):
        # برای مقایسه در صف اولویت (heapq)
        return self.f < other.f

    def __hash__(self):
        # برای اینکه بتوانیم گره‌ها را در یک Set (مانند closed_set) ذخیره کنیم
        return hash(self.position)

def a_star_search(
    start_pos: Tuple[int, int], 
    end_pos: Tuple[int, int], 
    obstacles: Set[Tuple[int, int]],
    grid_size: int = 10, # اندازه هر خانه گرید
    world_bounds: Tuple[int, int] = (800, 600) # ابعاد دنیا
) -> Optional[List[Tuple[int, int]]]:
    """
    الگوریتم مسیریابی A* برای پیدا کردن کوتاه‌ترین مسیر از نقطه شروع به پایان.

    :param start_pos: موقعیت شروع (x, y)
    :param end_pos: موقعیت هدف (x, y)
    :param obstacles: مجموعه‌ای از موقعیت‌های (x, y) که به عنوان مانع شناخته می‌شوند.
                      اینها مرکز خانه‌های گرید هستند که مسدود شده‌اند.
    :param grid_size: اندازه هر سلول در گرید برای گسسته‌سازی فضا.
    :param world_bounds: ابعاد کلی نقشه (width, height).
    :return: لیستی از نقاط مسیر از شروع تا پایان، یا None اگر مسیری پیدا نشود.
    """
    
    # گسسته‌سازی نقاط شروع و پایان برای قرارگیری روی گرید
    start_node = Node((round(start_pos[0] / grid_size), round(start_pos[1] / grid_size)))
    end_node = Node((round(end_pos[0] / grid_size), round(end_pos[1] / grid_size)))

    open_list = []      # صف اولویت برای گره‌هایی که باید بررسی شوند (heap)
    closed_set = set()  # مجموعه‌ی گره‌هایی که قبلا بررسی شده‌اند

    # اضافه کردن گره شروع به صف
    heapq.heappush(open_list, start_node)

    while open_list:
        # گرفتن گره با کمترین هزینه f از صف
        current_node = heapq.heappop(open_list)
        closed_set.add(current_node)

        # اگر به گره هدف رسیدیم، مسیر را بازسازی کن و برگردان
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                # تبدیل مختصات گرید به مختصات دنیای واقعی
                path.append((current.position[0] * grid_size, current.position[1] * grid_size))
                current = current.parent
            return path[::-1]  # مسیر را معکوس کن تا از شروع به پایان باشد

        # بررسی همسایه‌ها
        (x, y) = current_node.position
        # حرکت در 8 جهت (شامل حرکات مورب)
        neighbors_positions = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                               (x,     y - 1),             (x,     y + 1),
                               (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

        for next_pos in neighbors_positions:
            # بررسی اینکه آیا همسایه خارج از نقشه است
            if (next_pos[0] < 0 or next_pos[0] >= (world_bounds[0] / grid_size) or
                next_pos[1] < 0 or next_pos[1] >= (world_bounds[1] / grid_size)):
                continue

            # بررسی اینکه آیا همسایه یک مانع است
            if next_pos in obstacles:
                continue

            neighbor_node = Node(next_pos, current_node)

            # اگر همسایه قبلا بررسی شده، از آن صرف نظر کن
            if neighbor_node in closed_set:
                continue

            # محاسبه هزینه‌ها
            # هزینه حرکت از گره فعلی تا همسایه (1 برای افقی/عمودی، sqrt(2) برای مورب)
            move_cost = math.sqrt((neighbor_node.position[0] - current_node.position[0])**2 + 
                                  (neighbor_node.position[1] - current_node.position[1])**2)
            neighbor_node.g = current_node.g + move_cost
            
            # تخمین هیوریستیک (فاصله اقلیدسی تا هدف)
            neighbor_node.h = math.sqrt((neighbor_node.position[0] - end_node.position[0])**2 + 
                                        (neighbor_node.position[1] - end_node.position[1])**2)
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            # اگر همسایه در open_list است و مسیر جدید بهتر است، آن را آپدیت کن
            for open_node in open_list:
                if neighbor_node == open_node and neighbor_node.g > open_node.g:
                    break # مسیر فعلی بهتر است، پس این همسایه را نادیده بگیر
            else:
                # اگر همسایه در open_list نیست یا مسیر جدید بهتر است، آن را اضافه کن
                heapq.heappush(open_list, neighbor_node)

    return None # اگر حلقه تمام شد و به هدف نرسیدیم، یعنی مسیری وجود ندارد
