# skymind_sim/core/environment.py

from .drone import Drone

class Environment:
    """
    محیط شبیه‌سازی را تعریف می‌کند که شامل پهپادها و ابعاد فیزیکی است.
    
    Attributes:
        width (float): عرض محیط در محور X.
        height (float): طول محیط در محور Y.
        depth (float): ارتفاع محیط در محور Z.
        drones (dict): دیکشنری برای نگهداری پهپادها با استفاده از شناسه آن‌ها به عنوان کلید.
                       {drone_id: Drone_object}
    """
    
    def __init__(self, width: float, height: float, depth: float):
        self.width = width
        self.height = height
        self.depth = depth
        self.drones = {} # استفاده از دیکشنری برای دسترسی سریع‌تر

    def add_drone(self, drone: Drone):
        """یک پهپاد به محیط اضافه می‌کند."""
        # --- اینجا محل اصلاح است ---
        if drone.drone_id in self.drones:
            raise ValueError(f"Drone with ID {drone.drone_id} already exists in the environment.")
        self.drones[drone.drone_id] = drone

    def get_drone(self, drone_id: int) -> Drone | None:
        """یک پهپاد را با استفاده از شناسه آن برمی‌گرداند."""
        return self.drones.get(drone_id)

    def get_all_drones(self) -> list[Drone]:
        """لیستی از تمام پهپادهای موجود در محیط را برمی‌گرداند."""
        return list(self.drones.values())
