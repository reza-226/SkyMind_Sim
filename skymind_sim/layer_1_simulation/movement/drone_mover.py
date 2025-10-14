# ============================================
# D:\Payannameh\SkyMind_Sim\skymind_sim\layer_1_simulation\movement\drone_mover.py
# ============================================
# -*- coding: utf-8 -*-
import logging
from skymind_sim.layer_3_intelligence.pathfinding.path_planner import PathPlanner
from skymind_sim.layer_1_simulation.world.world import World


class DroneMover:
    def __init__(self, world: World):
        # دریافت منبع موانع و نقشه
        self.world = world
        self.path_planner = PathPlanner(world.grid_map, obstacles=world.obstacles)

    def _safe_plan_path(self, start, destination):
        """برنامه‌ریزی مسیر امن با بررسی بن‌بست"""
        try:
            return self.path_planner.plan_path(start, destination)
        except Exception as e:
            logging.error(f"Path planning failed: {e}")
            return [start]

    def move_drone(self, drone):
        """حرکت مرحله‌ای پهپاد با مدیریت مسیر"""
        if not drone.active or drone.position == drone.destination:
            return

        next_step = None

        # اگر مسیر از قبل وجود دارد
        if drone.path and len(drone.path) > 1:
            next_step = drone.path[1]
        else:
            # اگر مسیر خالی باشد، مسیر جدید ایجاد کن
            drone.path = self._safe_plan_path(drone.position, drone.destination)
            if len(drone.path) > 1:
                next_step = drone.path[1]

        # اگر گام بعدی موجود باشد و بدون برخورد
        if next_step:
            if not self.world.check_collision(next_step):
                drone.position = next_step
                drone.path_history.append(drone.position)  # 🟩 ثبت موقعیت جدید
                drone.path.pop(0)
                logging.debug(f"[{drone.id[:8]}] moved to {next_step}")
            else:
                drone.collision_avoided += 1
                drone.path = self._safe_plan_path(drone.position, drone.destination)
