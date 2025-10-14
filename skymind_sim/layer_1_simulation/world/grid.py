# =========================================================================
#  File: skymind_sim/layer_1_simulation/world/grid.py
#  Author: Reza & AI Assistant | 2025-10-14 (Refactored Version)
# =========================================================================
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

class Cell:
    """
    نماینده یک سلول واحد در گرید.
    این کلاس اطلاعات مکانی و وضعیت (مانند مانع بودن) را نگهداری می‌کند.
    """
    def __init__(self, x: int, y: int, is_obstacle: bool = False):
        self.x = x
        self.y = y
        self.is_obstacle = is_obstacle
        self.cost = 1  # هزینه پایه برای عبور از این سلول (برای الگوریتم‌های مسیریابی)

    def __repr__(self) -> str:
        return f"Cell({self.x}, {self.y}, Obstacle: {self.is_obstacle})"


class Grid:
    """
    ساختار داده‌ای برای نمایش دنیای شبیه‌سازی به صورت یک گرید دو بعدی.
    این کلاس یک مؤلفه "منفعل" است و هیچ منطق فعالی مانند زمان‌بندی (Scheduling) ندارد.
    وظیفه آن نگهداری اطلاعات مربوط به نقشه و وضعیت سلول‌ها (مانند موانع) است.
    """
    def __init__(self, width: int, height: int, cell_size: int):
        """
        سازنده کلاس گرید.
        
        Args:
            width (int): تعداد سلول‌ها در راستای افقی.
            height (int): تعداد سلول‌ها در راستای عمودی.
            cell_size (int): اندازه هر سلول بر حسب پیکسل (برای استفاده در رندر).
        """
        if not all(isinstance(i, int) and i > 0 for i in [width, height, cell_size]):
            raise ValueError("Grid dimensions and cell_size must be positive integers.")
            
        self.width = width
        self.height = height
        self.cell_size = cell_size
        
        # ایجاد یک ماتریس دو بعدی از اشیاء Cell
        self.cells: List[List[Cell]] = [
            [Cell(x, y) for y in range(height)] for x in range(width)
        ]
        logger.info(f"Grid created successfully with dimensions {width}x{height} and cell size {cell_size}px.")

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """
        یک سلول خاص را از گرید بر اساس مختصات آن برمی‌گرداند.
        
        Args:
            x (int): مختصات افقی سلول (ستون).
            y (int): مختصات عمودی سلول (سطر).
            
        Returns:
            Optional[Cell]: شیء سلول در صورت معتبر بودن مختصات، در غیر این صورت None.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[x][y]
        return None

    def set_obstacle(self, x: int, y: int, is_obstacle: bool = True):
        """یک سلول را به عنوان مانع (یا غیرمانع) علامت‌گذاری می‌کند."""
        cell = self.get_cell(x, y)
        if cell:
            cell.is_obstacle = is_obstacle
        else:
            logger.warning(f"Attempted to set obstacle at invalid grid coordinate: ({x}, {y})")

    def is_obstacle(self, x: int, y: int) -> bool:
        """
        بررسی می‌کند که آیا یک سلول مانع است یا خیر.
        مختصات خارج از گرید به عنوان مانع در نظر گرفته می‌شوند.
        """
        cell = self.get_cell(x, y)
        # اگر سلول وجود نداشته باشد (خارج از محدوده)، آن را به عنوان مانع در نظر بگیر.
        return cell.is_obstacle if cell else True

    def get_neighbors(self, cell: Cell) -> List[Cell]:
        """
        همسایه‌های معتبر (غیرمانع و داخل گرید) یک سلول را برای مسیریابی برمی‌گرداند.
        این متد همسایه‌های هشت‌جهته را بررسی می‌کند.
        """
        neighbors: List[Cell] = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # از خود سلول صرف‌نظر کن
                if dx == 0 and dy == 0:
                    continue

                nx, ny = cell.x + dx, cell.y + dy

                # بررسی کن که آیا همسایه داخل مرزهای گرید است
                neighbor_cell = self.get_cell(nx, ny)
                if neighbor_cell and not neighbor_cell.is_obstacle:
                    neighbors.append(neighbor_cell)
        return neighbors
