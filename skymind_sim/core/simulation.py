# skymind_sim/core/simulation.py

import time
import heapq
import numpy as np

from .environment import Environment
from .drone import Drone
from .event import Event, EventType
from .visualizer import Visualizer

class Simulation:
    def __init__(self, env: Environment, drones: dict[str, Drone], viz_enabled: bool = True):
        self.env = env
        self.drones = drones
        self.current_time = 0.0
        self.event_queue = []
        self.viz_enabled = viz_enabled
        self.visualizer = None

        if self.viz_enabled:
            # --- THIS IS THE CORRECTED LINE ---
            self.visualizer = Visualizer(size=env.size, drones=self.drones)

    def _schedule_event(self, timestamp: float, event_type: EventType, data: dict = None):
        """Adds an event to the priority queue."""
        event = Event(timestamp, event_type, data)
        heapq.heappush(self.event_queue, event)

    def run(self, until: float):
        """Runs the simulation until a specific time."""
        print(f"Starting simulation. Running until time {until}s.")

        # Schedule initial update events for all drones
        for drone_id in self.drones:
            self._schedule_event(self.current_time, EventType.UPDATE_STATE, {"drone_id": drone_id})

        # Schedule the first visualizer update
        if self.viz_enabled:
            self._schedule_event(self.current_time, EventType.VISUALIZER_UPDATE)

        running = True
        while self.event_queue and self.current_time < until and running:
            event = heapq.heappop(self.event_queue)
            
            # Clamp the time to the 'until' value to avoid overshooting
            self.current_time = min(event.timestamp, until)
            
            # --- Event Handling ---
            if event.event_type == EventType.UPDATE_STATE:
                drone_id = event.data["drone_id"]
                drone = self.drones[drone_id]
                
                # Calculate time delta for this drone's update
                # Note: This is a simplified approach. A more robust sim would track last update time.
                dt = 0.1 # Using a fixed time step for state updates
                drone.update(dt)
                print(f"[T={self.current_time:.2f}] Updated state for {drone.id}. Pos: {drone.pos}")

                # Schedule the next update for this drone
                if not drone.is_mission_complete():
                    self._schedule_event(self.current_time + dt, EventType.UPDATE_STATE, {"drone_id": drone_id})

            elif event.event_type == EventType.VISUALIZER_UPDATE:
                if self.visualizer:
                    running = self.visualizer.update() # No need to pass drones here anymore
                    if not running:
                         print("Visualizer window closed by user.")

                    # Schedule the next visual update only if sim is still running
                    if running:
                        viz_update_interval = 1.0 / 30.0 # ~30 FPS
                        self._schedule_event(self.current_time + viz_update_interval, EventType.VISUALIZER_UPDATE)

        print("Simulation finished.")
        if self.visualizer:
            self.visualizer.close()
