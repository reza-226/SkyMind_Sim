# skymind_sim/core/path_planner.py

import heapq
from .environment import Environment

class PathPlanner:
    """
    کلاسی برای برنامه‌ریزی مسیر با استفاده از الگوریتم A*.
    این کلاس یک شیء Environment دریافت می‌کند و از آن برای مسیریابی استفاده می‌کند.
    """
    def __init__(self, environment: Environment):
        """
        سازنده کلاس PathPlanner.

        Args:
            environment (Environment): شیء محیط که شامل موانع و ابعاد است.
        """
        self.env = environment
        print("PathPlanner initialized.")

    def _heuristic(self, a: tuple, b: tuple) -> float:
        """
        محاسبه فاصله اقلیدسی (Heuristic) بین دو نقطه در فضای سه‌بعدی.
        این تابع هزینه تخمینی رسیدن از نقطه a به نقطه b را محاسبه می‌کند.
        """
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5

    def _get_neighbors(self, point: tuple) -> list:
        """
        همسایه‌های معتبر یک نقطه را پیدا می‌کند.
        همسایه‌ها شامل 26 جهت ممکن در یک شبکه سه‌بعدی هستند (حرکت مستقیم و قطری).
        """
        x, y, z = point
        neighbors = []
        # بررسی تمام 26 جهت ممکن در اطراف نقطه فعلی
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == 0 and dy == 0 and dz == 0:
                        continue  # خود نقطه را به عنوان همسایه در نظر نگیر
                    
                    neighbor = (x + dx, y + dy, z + dz)
                    
                    # فقط همسایه‌هایی که در محدوده نقشه هستند و مانع نیستند را اضافه کن
                    if self.env.is_valid_point(neighbor):
                        neighbors.append(neighbor)
        return neighbors

    def _reconstruct_path(self, came_from: dict, current: tuple) -> list:
        """
        مسیر را از نقطه پایان به نقطه شروع بازسازی می‌کند.
        """
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1]  # مسیر را برعکس کن تا از شروع به پایان باشد

    def plan_path(self, start: tuple, end: tuple) -> list | None:
        """
        الگوریتم A* را برای یافتن کوتاه‌ترین مسیر از نقطه شروع به پایان اجرا می‌کند.

        Args:
            start (tuple): مختصات نقطه شروع (x, y, z).
            end (tuple): مختصات نقطه هدف (x, y, z).

        Returns:
            list | None: لیستی از تاپل‌ها که مسیر را نشان می‌دهند، یا None اگر مسیری یافت نشود.
        """
        if not self.env.is_valid_point(start) or not self.env.is_valid_point(end):
            print(f"Error: Start point {start} or end point {end} is invalid (outside bounds or inside an obstacle).")
            return None

        open_set = [(0, start)]  # (f_score, point)
        heapq.heapify(open_set)
        
        came_from = {}
        
        g_score = {start: 0} # هزینه واقعی از شروع تا هر نقطه
        f_score = {start: self._heuristic(start, end)} # هزینه تخمینی کل (g_score + heuristic)

        open_set_hash = {start} # برای جستجوی سریع در open_set
        
        nodes_explored = 0

        print(f"Starting A* from {start} to {end}...")

        while open_set:
            nodes_explored += 1
            # نمایش پیشرفت برای جلوگیری از حس توقف برنامه
            if nodes_explored % 5000 == 0:
                print(f"  ... explored {nodes_explored} nodes.")

            current = heapq.heappop(open_set)[1]
            open_set_hash.remove(current)

            if current == end:
                print(f"Path found! Total nodes explored: {nodes_explored}")
                return self._reconstruct_path(came_from, current)

            for neighbor in self._get_neighbors(current):
                # هزینه حرکت از current به neighbor همیشه 1 است (یا جذر 2 و 3 برای حرکات قطری)
                # برای سادگی، هزینه حرکت به هر همسایه را برابر فاصله اقلیدسی در نظر می‌گیریم
                tentative_g_score = g_score[current] + self._heuristic(current, neighbor)
                
                # اگر مسیر جدید به همسایه بهتر است یا هنوز مسیری برای آن پیدا نشده
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self._heuristic(neighbor, end)
                    
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)
        
        print(f"No path could be found after exploring {nodes_explored} nodes.")
        return None
