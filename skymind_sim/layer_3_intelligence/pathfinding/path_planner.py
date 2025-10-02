# مسیر: skymind_sim/layer_3_intelligence/pathfinding/path_planner.py

import numpy as np
import logging
from typing import Optional, List, Dict, Any
from .a_star import a_star

class PathPlanner:
    """
    مسئول برنامه‌ریزی مسیر برای پهپادها با استفاده از الگوریتم A*.
    این کلاس یک گرید دو بعدی از دنیا می‌سازد و موانع را در آن مشخص می‌کند.
    """
    def __init__(self, world_dim: tuple[int, int], obstacles: List[Dict[str, Any]]):
        """
        سازنده کلاس PathPlanner.

        Args:
            world_dim (tuple[int, int]): ابعاد دنیا به صورت (عرض, ارتفاع).
            obstacles (List[Dict[str, Any]]): لیستی از دیکشنری‌ها که هر کدام یک مانع را توصیف می‌کنند.
        """
        self.world_dim = world_dim
        self.obstacles = obstacles
        self.logger = logging.getLogger(__name__)
        self.grid = self._create_pathfinding_grid()
        self.logger.info(f"PathPlanner با یک گرید به ابعاد {self.grid.shape} راه‌اندازی شد.")

    def _create_pathfinding_grid(self) -> np.ndarray:
        """
        یک گرید دو بعدی از دنیا ایجاد می‌کند. مقدار 0 برای فضای قابل عبور و 1 برای مانع است.
        """
        width, height = self.world_dim
        # گرید با مقدار صفر (قابل عبور) ساخته می‌شود. ترتیب NumPy: (ارتفاع, عرض)
        grid = np.zeros((height, width), dtype=np.int8)
        self.logger.info(f"در حال ساخت گرید مسیریابی با ابعاد {height}x{width}.")

        for obs_data in self.obstacles:
            # فرض می‌کنیم موانع از نوع مستطیلی ('rect') هستند.
            if obs_data.get('type') == 'rect':
                try:
                    x, y, w, h = obs_data['rect']
                    # محدود کردن مختصات به ابعاد گرید
                    x_start, y_start = max(0, x), max(0, y)
                    x_end, y_end = min(width, x + w), min(height, y + h)
                    
                    # علامت‌گذاری ناحیه مانع با مقدار 1.
                    # در NumPy، اندیس اول ردیف (y) و اندیس دوم ستون (x) است.
                    grid[y_start:y_end, x_start:x_end] = 1
                    self.logger.debug(f"مانع در ناحیه [y:{y_start}-{y_end}, x:{x_start}-{x_end}] علامت‌گذاری شد.")
                except (KeyError, IndexError) as e:
                    self.logger.warning(f"خطا در پردازش داده مانع مستطیلی {obs_data}: {e}")
            else:
                self.logger.warning(f"نادیده گرفتن مانع با نوع ناشناخته یا فرمت نادرست: {obs_data.get('type')}")
        
        return grid

    def find_path(self, start: tuple[int, int], goal: tuple[int, int]) -> Optional[list[tuple[int, int]]]:
        """
        کوتاه‌ترین مسیر بین دو نقطه با استفاده از الگوریتم A* را پیدا می‌کند.
        
        Args:
            start (tuple[int, int]): مختصات نقطه شروع (ردیف، ستون).
            goal (tuple[int, int]): مختصات نقطه هدف (ردیف، ستون).

        Returns:
            یک لیست از نقاط مسیر یا None در صورت عدم وجود مسیر.
        """
        self.logger.info(f"در جستجوی مسیر از {start} به {goal}")
        
        # اعتبارسنجی نقاط شروع و پایان
        rows, cols = self.grid.shape
        if not (0 <= start[0] < rows and 0 <= start[1] < cols):
            self.logger.error(f"نقطه شروع {start} خارج از محدوده گرید است.")
            return None
        if not (0 <= goal[0] < rows and 0 <= goal[1] < cols):
            self.logger.error(f"نقطه هدف {goal} خارج از محدوده گرید است.")
            return None
        
        if self.grid[start] == 1:
            self.logger.warning(f"نقطه شروع {start} درون یک مانع قرار دارد.")
            return None
        if self.grid[goal] == 1:
            self.logger.warning(f"نقطه هدف {goal} درون یک مانع قرار دارد.")
            return None

        path = a_star(self.grid, start, goal)
        
        if path:
            self.logger.info(f"مسیر با {len(path)} گام پیدا شد.")
        else:
            self.logger.warning(f"مسیری از {start} به {goal} یافت نشد.")
            
        return path
