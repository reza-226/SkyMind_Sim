# ============================================
# D:\Payannameh\SkyMind_Sim\skymind_sim\layer_1_simulation\entities\drone.py
# ============================================

import time

class Drone:
    def __init__(self, drone_id, start_pos, destination,
                 battery_capacity, energy_consumption_rate,
                 max_speed, communication_delay,
                 exec_level="Local", metrics_collector=None):
        self.id = drone_id
        self.position = start_pos
        self.destination = destination

        self.battery_capacity = battery_capacity
        self.energy_consumption_rate = energy_consumption_rate
        self.max_speed = max_speed
        self.communication_delay = communication_delay
        self.exec_level = exec_level
        self.metrics_collector = metrics_collector

        # مسیر فعلی پهپاد (توسط DroneMover محاسبه می‌شود)
        self.path = []
        self.distance_travelled = 0.0
        self.battery_remaining = battery_capacity
        self.start_time = time.time()

        # متریک‌های مأموریت
        self.stop_count = 0
        self.collision_avoided = 0

        # ارتباطات
        self.received_messages = []
        self.neighbors = []

    def update_metrics_on_arrival(self):
        mission_time = time.time() - self.start_time
        if self.metrics_collector:
            self.metrics_collector.log_task(
                drone_id=self.id,
                exec_level=self.exec_level,
                path=self.path,
                distance=self.distance_travelled,
                battery_remaining=self.battery_remaining,
                total_time=mission_time,
                stop_count=self.stop_count,
                collision_avoided=self.collision_avoided
            )

    def receive_message(self, msg, latency, success):
        self.received_messages.append({
            "from_exec_level": msg.get("exec_level", None),
            "battery_report": msg.get("battery", None),
            "latency": latency,
            "success": success
        })
        if self.metrics_collector:
            self.metrics_collector.log_network_event(
                drone_id=self.id,
                latency=latency,
                success=success,
                neighbors_count=len(self.neighbors)
            )
