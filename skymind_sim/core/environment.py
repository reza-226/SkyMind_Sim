# skymind_sim/core/environment.py

import numpy as np
from typing import List, Tuple

# ایمپورت‌های نسبی برای ماژول‌های درون پکیج core
from .drone import Drone
from .path_planner import PathPlanner

class Obstacle:
    """یک کلاس پایه برای همه موانع."""
    def is_inside(self, point: np.ndarray) -> bool:
        raise NotImplementedError

class BoxObstacle(Obstacle):
    """یک مانع مکعبی شکل."""
    def __init__(self, position: np.ndarray, size: np.ndarray):
        self.position = position
        self.size = size
        self.min_corner = position - size / 2
        self.max_corner = position + size / 2

    def is_inside(self, point: np.ndarray) -> bool:
        return np.all(point >= self.min_corner) and np.all(point <= self.max_corner)

class Environment:
    """
    کلاس محیط شبیه‌سازی که شامل پهپادها و موانع است.
    """
    def __init__(self, dimensions: Tuple[float, float, float], obstacles: List[Obstacle] = None):
        self.dimensions = np.array(dimensions)
        self.obstacles = obstacles if obstacles is not None else []
        self.drones: List['Drone'] = [] # استفاده از 'Drone' برای جلوگیری از circular import
        
        # ایجاد نمونه مسیریاب با دقت 0.5 متر برای گرید
        self.path_planner = PathPlanner(self, grid_resolution=0.5)

    def add_drone(self, drone: 'Drone'):
        self.drones.append(drone)
        drone.set_environment(self)

    def update(self, dt: float):
        for drone in self.drones:
            drone.update(dt)
        self.check_collisions()

    def check_collisions(self):
        for i, drone1 in enumerate(self.drones):
            # بررسی برخورد با موانع
            for obstacle in self.obstacles:
                if obstacle.is_inside(drone1.position):
                    print(f"Collision Detected! Drone {drone1.id} hit an obstacle at {drone1.position}.")
            
            # بررسی برخورد پهپاد با پهپاد (اختیاری)
            for j in range(i + 1, len(self.drones)):
                drone2 = self.drones[j]
                distance = np.linalg.norm(drone1.position - drone2.position)
                if distance < (drone1.size + drone2.size):
                    print(f"Collision Detected! Drone {drone1.id} and Drone {drone2.id} collided.")
