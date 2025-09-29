# skymind_sim/core/environment.py

import numpy as np
from typing import List, Dict, Any

# برای جلوگیری از خطای Circular Import، کلاس Drone را فقط برای Type Hinting وارد می‌کنیم
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from skymind_sim.core.drone import Drone

class Environment:
    """
    محیط شبیه‌سازی را تعریف می‌کند که شامل ابعاد، پهپادها و موانع است.
    """
    def __init__(self, dimensions: np.ndarray):
        """
        سازنده کلاس Environment.

        Args:
            dimensions (np.ndarray): آرایه NumPy با ابعاد [طول, عرض, ارتفاع] محیط.
        """
        if not isinstance(dimensions, np.ndarray) or dimensions.shape != (3,):
            raise ValueError("dimensions باید یک آرایه NumPy با سه عنصر باشد.")
        if np.any(dimensions <= 0):
            raise ValueError("ابعاد محیط باید مقادیر مثبت داشته باشند.")
            
        self._dimensions = dimensions
        self._drones: List['Drone'] = []
        self._obstacles: List[Dict[str, Any]] = []

    @property
    def dimensions(self) -> np.ndarray:
        return self._dimensions

    @property
    def drones(self) -> List['Drone']:
        return self._drones

    @property
    def obstacles(self) -> List[Dict[str, Any]]:
        return self._obstacles

    def add_drone(self, drone: 'Drone'):
        """یک پهپاد به محیط اضافه می‌کند."""
        # در آینده می‌توانیم بررسی کنیم که آیا پهپاد از نوع Drone است یا خیر
        if drone not in self._drones:
            self._drones.append(drone)

    def add_obstacle(self, center: np.ndarray, radius: float):
        """یک مانع کروی به محیط اضافه می‌کند."""
        if not isinstance(center, np.ndarray) or center.shape != (3,):
            raise ValueError("مرکز مانع باید یک آرایه NumPy سه‌بعدی باشد.")
        if not isinstance(radius, (int, float)) or radius <= 0:
            raise ValueError("شعاع مانع باید یک عدد مثبت باشد.")
            
        obstacle = {'center': center, 'radius': radius}
        self._obstacles.append(obstacle)

    def check_collisions(self) -> List[Dict[str, Any]]:
        """
        بررسی می‌کند که آیا هیچ پهپادی با هیچ مانعی برخورد کرده است یا خیر.

        Returns:
            لیستی از دیکشنری‌ها، که هر کدام اطلاعات برخورد را شامل می‌شود.
            مثال: [{'drone_id': 'd1', 'obstacle_index': 0}]
        """
        collisions = []
        for drone in self._drones:
            for i, obstacle in enumerate(self._obstacles):
                distance = np.linalg.norm(drone.position - obstacle['center'])
                if distance <= obstacle['radius']:
                    collisions.append({
                        'drone_id': drone.drone_id,
                        'obstacle_index': i
                    })
        return collisions
        
    def __repr__(self) -> str:
        return (f"Environment(dimensions={list(self.dimensions)}, "
                f"num_drones={len(self.drones)}, "
                f"num_obstacles={len(self.obstacles)})")
