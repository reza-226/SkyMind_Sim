# skymind_sim/core/simulation.py

import time
from .drone import Drone
from .environment import Environment
from .event import Event, EventType
from .scheduler import Scheduler

class Simulation:
    def __init__(self, drones: list[Drone], environment: Environment, time_step: float = 0.1):
        self.drones = {drone.drone_id: drone for drone in drones}
        self.environment = environment
        self.time_step = time_step
        self.scheduler = Scheduler()
        self.start_time = 0
        self.current_time = 0
        
        for drone_id in self.drones:
            initial_event = Event(
                time=self.current_time,
                type=EventType.DRONE_UPDATE,
                drone_id=drone_id
            )
            # This call MUST match the method name in scheduler.py
            self.scheduler.add_event(initial_event)
        
        print("--- Simulation Starting ---")

    def _update_drone_and_reschedule(self, event: Event):
        drone = self.drones.get(event.drone_id)
        
        if drone and drone.status == "flying":
            drone.update_state(self.time_step)
            
            next_event = Event(
                time=self.current_time + self.time_step,
                type=EventType.DRONE_UPDATE,
                drone_id=drone.drone_id
            )
            # This call MUST match the method name in scheduler.py
            self.scheduler.add_event(next_event)

    def run(self):
        self.start_time = time.time()
        
        while not self.scheduler.is_empty():
            event = self.scheduler.get_next_event()
            if not event: break

            self.current_time = event.time

            if event.type == EventType.DRONE_UPDATE:
                if event.drone_id in self.drones:
                    self._update_drone_and_reschedule(event)
        
        end_time = time.time()
        print("\n--- Simulation Finished: No more events in the queue ---")
        self.print_summary(end_time - self.start_time)

    def print_summary(self, real_time_elapsed: float):
        print("\n--- Simulation Summary ---")
        print(f"Total Real Time Elapsed: {real_time_elapsed:.2f} seconds")
        print(f"Total Mission Time: {self.current_time:.2f} seconds")
        print("\n--- Final Drone States ---")
        for drone_id, drone in self.drones.items():
            print(f"  Drone ID: {drone_id}")
            print(f"    Final Status: {drone.status}")
            print(f"    Final Position: {drone.pos}")
            print(f"    Remaining Battery: {drone.battery.level:.2f}%")
            print("--------------------")
