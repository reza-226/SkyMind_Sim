# skymind_sim/core/simulation.py

import numpy as np
from .environment import Environment
from .drone import Drone, DroneStatus

class Simulation:
    def __init__(self, environment: Environment):
        self.environment = environment
        self.time = 0.0
        # --- اصلاح برای خواندن از متد جدید ---
        self.history = {drone.drone_id: [] for drone in self.environment.get_all_drones()}

    def _record_state(self):
        """وضعیت فعلی همه پهپادها را ثبت می‌کند."""
        # --- اصلاح برای خواندن از متد جدید ---
        for drone in self.environment.get_all_drones():
            pos = drone.position
            self.history[drone.drone_id].append(
                (self.time, pos[0], pos[1], pos[2])
            )

    def _update_drone_state(self, drone: Drone, dt: float):
        """منطق هدایت و به‌روزرسانی وضعیت پهپاد را پیاده‌سازی می‌کند."""
        if drone.status != DroneStatus.FLYING:
            return

        if drone.destination is None:
            return

        direction_vector = drone.destination - drone.position
        distance_to_destination = np.linalg.norm(direction_vector)

        if distance_to_destination < drone.target_speed * dt:
            drone.move_to(drone.destination)
            drone.set_velocity(np.zeros(3))
            drone.status = DroneStatus.HOVERING
            return

        normalized_direction = direction_vector / distance_to_destination
        new_velocity = normalized_direction * drone.target_speed
        drone.set_velocity(new_velocity)
        
        new_position = drone.position + drone.velocity * dt
        drone.move_to(new_position)

    def run(self, num_steps: int, dt: float = 0.1):
        """شبیه‌سازی را برای تعداد مراحل مشخص اجرا می‌کند."""
        print(f"Running simulation for {num_steps} steps with dt={dt}...")
        self._record_state() 

        for step in range(num_steps):
            self.time += dt
            # --- اصلاح برای خواندن از متد جدید ---
            for drone in self.environment.get_all_drones():
                self._update_drone_state(drone, dt)
            
            self._record_state() 
        
        print("Simulation finished.")
