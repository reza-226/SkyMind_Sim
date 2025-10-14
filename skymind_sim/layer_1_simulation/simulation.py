# skymind_sim/layer_1_simulation/simulation.py
from typing import Any, Dict
from ..layer_2_models.grid import Grid
from ..utils.logger import LogManager

class Simulation:
    def __init__(self, map_filename: str):
        """
        شبیه‌ساز را با بارگذاری گرید مقداردهی اولیه می‌کند.
        این کلاس دیگر لاگر را به عنوان ورودی نمی‌گیرد.
        """
        # لاگر مورد نیاز خود را مستقیماً از LogManager دریافت می‌کند
        self.logger = LogManager.get_logger("Simulation")
        
        # همان لاگر را به Grid پاس می‌دهد (اگر Grid به آن نیاز دارد)
        self.grid = Grid(map_filename=map_filename, logger=self.logger)
        
        self.logger.info("Simulation initialized.")

    @property
    def grid_dimensions(self) -> tuple[int, int]:
        """طول و عرض گرید را برمی‌گرداند."""
        return self.grid.width, self.grid.height

    def run_step(self):
        """یک گام از منطق شبیه‌سازی را اجرا می‌کند."""
        # در آینده اینجا منطق حرکت پهپادها و ... اضافه می‌شود
        pass

    def get_world_state(self) -> Dict[str, Any]:
        """وضعیت فعلی دنیای شبیه‌سازی را جمع‌آوری و برمی‌گرداند."""
        return {
            "grid_width": self.grid.width,
            "grid_height": self.grid.height,
            "obstacles": list(self.grid.obstacles),
            "drones": [],  # در آینده اطلاعات پهپادها اینجا قرار می‌گیرد
            "goals": self.grid.goals,
            "cell_size": self.grid.cell_size,
        }
