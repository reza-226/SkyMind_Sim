# ============================================
# D:\Payannameh\SkyMind_Sim\skymind_sim\utils\metrics.py
# ============================================

import csv

class MetricsCollector:
    def __init__(self):
        self.drone_tasks = []
        self.network_events = []

    def log_task(self, drone_id, exec_level, path, distance, battery_remaining,
                 total_time, stop_count, collision_avoided):
        self.drone_tasks.append({
            "DroneID": drone_id,
            "ExecLevel": exec_level,
            "Path": path,
            "DistanceTravelled": distance,
            "BatteryRemaining": battery_remaining,
            "TotalMissionTime": total_time,
            "StopCount": stop_count,
            "CollisionAvoided": collision_avoided
        })

    def log_network_event(self, drone_id, latency, success, neighbors_count):
        self.network_events.append({
            "DroneID": drone_id,
            "Latency": latency,
            "CommSuccess": success,
            "NeighborCount": neighbors_count
        })

    def export_csv(self, filename):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "DroneID", "ExecLevel", "Path", "DistanceTravelled",
                "BatteryRemaining", "TotalMissionTime", "StopCount", "CollisionAvoided",
                "Latency", "CommSuccess", "NeighborCount"
            ])
            for task in self.drone_tasks:
                related_events = [e for e in self.network_events if e["DroneID"] == task["DroneID"]]
                if related_events:
                    for e in related_events:
                        writer.writerow([
                            task["DroneID"], task["ExecLevel"], task["Path"],
                            task["DistanceTravelled"], task["BatteryRemaining"],
                            task["TotalMissionTime"], task["StopCount"], task["CollisionAvoided"],
                            e["Latency"], e["CommSuccess"], e["NeighborCount"]
                        ])
                else:
                    writer.writerow([
                        task["DroneID"], task["ExecLevel"], task["Path"],
                        task["DistanceTravelled"], task["BatteryRemaining"],
                        task["TotalMissionTime"], task["StopCount"], task["CollisionAvoided"],
                        None, None, None
                    ])
