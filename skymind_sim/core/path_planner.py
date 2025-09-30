# skymind_sim/core/path_planner.py

import numpy as np

class PathPlanner:
    """
    این کلاس مسئول پیدا کردن مسیر از نقطه شروع به نقطه پایان در محیط است.
    در حال حاضر از یک الگوریتم ساده استفاده می‌کند، اما می‌تواند برای الگوریتم‌های
    پیچیده‌تر مانند A*، RRT* و غیره گسترش یابد.
    """

    def __init__(self, environment):
        """
        سازنده کلاس PathPlanner.

        Args:
            environment (Environment): شیء محیط که شامل گرید موانع، نقطه شروع و پایان است.
        """
        self.env = environment
        self.start_node = self.env.world_to_grid(self.env.start_point)
        self.goal_node = self.env.world_to_grid(self.env.end_point)
        
        print("PathPlanner initialized.")
        print(f"Start node (grid coords): {self.start_node}")
        print(f"Goal node (grid coords): {self.goal_node}")


    def find_path(self):
        """
        الگوریتم مسیریابی را برای پیدا کردن مسیر اجرا می‌کند.
        
        TODO: الگوریتم واقعی (مانند A*) در اینجا پیاده‌سازی شود.
        
        Returns:
            list: لیستی از نقاط (به صورت مختصات دنیای واقعی) که مسیر را تشکیل می‌دهند،
                  یا None اگر مسیری پیدا نشود.
        """
        print("Searching for a path...")

        # بررسی اولیه: آیا نقطه شروع یا پایان داخل مانع است؟
        if self.env.is_obstacle(self.start_node):
            print("Error: Start node is inside an obstacle.")
            return None
        if self.env.is_obstacle(self.goal_node):
            print("Error: Goal node is inside an obstacle.")
            return None

        # --- منطق مسیریابی موقت ---
        # در این مرحله، فقط یک مسیر مستقیم فرضی برمی‌گردانیم تا جریان برنامه تست شود.
        # این مسیر شامل نقطه شروع و پایان است.
        # در آینده این بخش با الگوریتم A* جایگزین خواهد شد.
        
        print("Temporary path generation: Creating a direct line for testing purposes.")
        
        # تبدیل گره‌های شروع و پایان به مختصات دنیای واقعی
        start_world = self.env.grid_to_world(self.start_node)
        goal_world = self.env.grid_to_world(self.goal_node)
        
        # ایجاد یک مسیر ساده شامل دو نقطه
        path_in_world_coords = [start_world.tolist(), goal_world.tolist()]

        return path_in_world_coords
