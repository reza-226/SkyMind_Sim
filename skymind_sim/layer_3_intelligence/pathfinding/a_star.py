import heapq
import logging
from typing import List, Tuple, Optional

# اصلاح کلیدی: ایمپورت مطلق از ریشه پکیج برای جلوگیری از خطای
# "attempted relative import beyond top-level package"
from skymind_sim.layer_1_simulation.world.grid import Grid

# دریافت لاگر برای ثبت اطلاعات این ماژول
logger = logging.getLogger(__name__)

class Node:
    """
    یک کلاس کمکی برای نمایش یک گره در جستجوی A*.
    حاوی موقعیت، گره والد و هزینه‌های g, h, f است.
    """
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0  # هزینه از گره شروع تا گره فعلی
        self.h = 0  # هزینه تخمینی (هیوریستیک) از گره فعلی تا گره هدف
        self.f = 0  # هزینه کل (f = g + h)

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f"Node(pos={self.position}, f={self.f})"


class AStarPlanner:
    """
    کلاس مسیریاب که الگوریتم A* را برای پیدا کردن کوتاه‌ترین مسیر در یک گرید پیاده‌سازی می‌کند.
    """

    def __init__(self, grid: Grid):
        """
        سازنده کلاس AStarPlanner.

        Args:
            grid (Grid): آبجکت گریدی که جستجو در آن انجام می‌شود.
        """
        if not isinstance(grid, Grid):
            raise TypeError(f"AStarPlanner expects a Grid object, but got {type(grid)}")
        self.grid = grid
        logger.info(f"AStarPlanner initialized with a grid of size ({self.grid.width}, {self.grid.height})")

    def plan_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        محاسبه کوتاه‌ترین مسیر بین دو نقطه با استفاده از الگوریتم A*.

        Args:
            start (Tuple[int, int]): مختصات نقطه شروع (x, y).
            end (Tuple[int, int]): مختصات نقطه هدف (x, y).

        Returns:
            List[Tuple[int, int]]: لیستی از مختصات (x, y) که مسیر از شروع به هدف را نشان می‌دهد.
                                    اگر مسیری پیدا نشود، لیست خالی برمی‌گرداند.
        """
        logger.debug(f"Planning path from {start} to {end}")

        # اطمینان از اینکه نقاط شروع و هدف معتبر هستند
        if not self.grid.is_walkable(start[0], start[1]) or not self.grid.is_walkable(end[0], end[1]):
            logger.warning(f"Start {start} or end {end} position is not walkable.")
            return []

        # ایجاد گره‌های شروع و هدف
        start_node = Node(None, start)
        end_node = Node(None, end)

        # لیست باز (open_list) برای گره‌هایی که باید بررسی شوند
        # و لیست بسته (closed_set) برای گره‌های بررسی شده
        open_list = []
        closed_set = set()

        # استفاده از heapq برای پیاده‌سازی صف اولویت (برای انتخاب گره با کمترین هزینه f)
        heapq.heappush(open_list, start_node)

        # حلقه اصلی تا زمانی که گره‌ای برای بررسی وجود داشته باشد
        while open_list:
            # دریافت گره با کمترین هزینه f از صف
            current_node = heapq.heappop(open_list)
            closed_set.add(current_node.position)

            # اگر به گره هدف رسیدیم، مسیر را بازسازی و برگردان
            if current_node == end_node:
                logger.info(f"Path found from {start} to {end}.")
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # مسیر را معکوس کن تا از شروع به هدف باشد

            # تولید گره‌های همسایه (حرکت در 8 جهت)
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # 8 جهت
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # اطمینان از اینکه همسایه در محدوده گرید است
                if not (0 <= node_position[0] < self.grid.width and 0 <= node_position[1] < self.grid.height):
                    continue

                # اطمینان از اینکه همسایه یک مانع نیست
                if not self.grid.is_walkable(node_position[0], node_position[1]):
                    continue
                
                # اگر همسایه قبلا بررسی شده، از آن صرف نظر کن
                if node_position in closed_set:
                    continue

                # ایجاد گره جدید
                new_node = Node(current_node, node_position)
                children.append(new_node)

            # پردازش همسایه‌ها
            for child in children:
                # محاسبه هزینه‌ها
                # هزینه حرکت قطری 1.4 و حرکت مستقیم 1 است
                move_cost = 1.4 if child.position[0] != current_node.position[0] and child.position[1] != current_node.position[1] else 1
                child.g = current_node.g + move_cost
                
                # هیوریستیک: فاصله اقلیدسی
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # اگر گره همسایه در لیست باز است و هزینه g فعلی بیشتر است، آن را به‌روز نکن
                if any(open_node for open_node in open_list if child == open_node and child.g > open_node.g):
                    continue

                # اضافه کردن همسایه به لیست باز
                heapq.heappush(open_list, child)

        logger.warning(f"No path found from {start} to {end}.")
        return [] # اگر حلقه تمام شد و به هدف نرسیدیم، یعنی مسیری وجود ندارد
