# ============================================================
#  File: environment.py
#  Layer: 0 - Presentation
#  Project: SkyMind_Sim
#  Author: Reza | 2025-10-13
#  Description:
#       ماژول محیط شبیه‌سازی شامل نقشه، پهپادها و موانع
# ============================================================

from skymind_sim.layer_1_simulation.world.obstacle import Obstacle
from skymind_sim.layer_1_simulation.entities.drone import Drone


class Environment:
    def __init__(self, map_data, logger=None):
        """
        ساخت محیط شبیه‌سازی بر اساس داده‌های نقشه JSON.
        """
        self.logger = logger
        self.map_data = map_data  # ✅ اضافه‌شده برای سازگاری با Renderer و Simulation

        # --- خواندن مشخصات نقشه ---
        self.width = map_data.get("width", 25)
        self.height = map_data.get("height", 20)
        self.cell_size = map_data.get("cell_size", 32)
        self.window_size = (
            self.width * self.cell_size,
            self.height * self.cell_size,
        )

        # --- ایجاد موانع و پهپادها ---
        self.obstacles = self._load_obstacles(map_data.get("obstacles", []))
        self.drones = self._load_drones(map_data.get("drones", []))

        if self.logger:
            self.logger.info(f"🌍 Environment ساخته شد | ابعاد: {self.width}x{self.height}")

    # --------------------------------------------------------
    # ساخت موانع از داده‌های JSON
    # --------------------------------------------------------
    def _load_obstacles(self, obstacle_data_list):
        obstacles = []
        for obs_data in obstacle_data_list:
            try:
                obstacle = Obstacle(
                    x=obs_data.get("x", 0),
                    y=obs_data.get("y", 0),
                    width=obs_data.get("width", 32),
                    height=obs_data.get("height", 32),
                )
                obstacles.append(obstacle)
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"⚠️ خطا در بارگذاری مانع: {e}")
        return obstacles

    # --------------------------------------------------------
    # ساخت پهپادها از داده‌های JSON
    # --------------------------------------------------------
    def _load_drones(self, drone_data_list):
        drones = []
        for dr_data in drone_data_list:
            try:
                drone = Drone(
                    id=dr_data.get("id", 0),
                    x=dr_data.get("x", 0),
                    y=dr_data.get("y", 0),
                    speed=dr_data.get("speed", 1.0),
                    color=dr_data.get("color", "#0077b6"),
                )
                drones.append(drone)
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"⚠️ خطا در بارگذاری پهپاد: {e}")
        return drones
