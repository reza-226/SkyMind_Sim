# ============================================================
#  File: path_planner.py
#  Layer: L3 - Intelligence (A* Path Planning)
#  Author: Reza – October 2025
# ============================================================

import math
from skymind_sim.layer_3_intelligence.pathfinding.a_star import AStar

class PathPlanner:
    """A* path planning manager for drones."""

    def __init__(self, environment):
        self.env = environment
        self.astar = AStar(environment)

    def find_nearest_goal(self, start):
        """
        Find the nearest goal (x, y) for the drone based on Euclidean distance.
        Compatible with Drone.compute_path().
        """
        goals = []
        # در محیط بررسی کن آیا پهپادها یا اهداف درون JSON تعریف شده‌اند
        for drone_data in getattr(self.env, "drones", []):
            if hasattr(drone_data, "goal"):
                goals.append(drone_data.goal)
            elif isinstance(drone_data, dict) and "goal" in drone_data:
                goals.append(drone_data["goal"])

        if not goals:
            return None

        # انتخاب نزدیک‌ترین هدف نسبت به نقطه شروع
        nearest = min(goals, key=lambda g: math.dist(start, (g["x"], g["y"])))
        return (nearest["x"], nearest["y"])

    def plan_path(self, start, goal):
        """
        Compute the A* path between start and goal positions.
        Returns a list of (x, y) coords.
        """
        if not goal:
            return []

        return self.astar.find_path(start, goal)
