# skymind_sim/core/simulation.py

import time
from .drone import Drone
from .environment import Environment
from .scheduler import Scheduler
from .event import Event

class Simulation:
    def __init__(self, environment: Environment, drones: list[Drone]):
        self.env = environment
        self.drones = {drone.drone_id: drone for drone in drones}
        self.scheduler = Scheduler()
        self.start_time_real = None
        
        # Simulation parameters
        self.time_step = 0.1 # seconds, granularity of simulation updates

    def _setup_initial_events(self):
        """Sets up the initial events for the simulation."""
        for drone_id, drone in self.drones.items():
            # Start the mission for the drone
            drone.start_mission()
            
            # Schedule the first update event for each drone
            if drone.status == "flying":
                initial_event = Event(
                    timestamp=self.scheduler.current_time,
                    priority=1,
                    action=self._update_drone_and_reschedule,
                    event_type='DRONE_UPDATE',
                    data={'drone_id': drone_id}
                )
                self.scheduler.schedule_event(initial_event)

    def _update_drone_and_reschedule(self, drone_id: str):
        """
        The core action for updating a drone's state and scheduling the next update.
        """
        drone = self.drones.get(drone_id)
        if not drone or drone.status not in ["flying", "hovering"]:
            # Stop rescheduling if drone is no longer active
            return

        # Perform the update for the time_step
        drone.update_state(self.time_step)

        # If the drone is still active, schedule the next update
        if drone.status in ["flying", "hovering"]:
            next_event_time = self.scheduler.current_time + self.time_step
            next_event = Event(
                timestamp=next_event_time,
                priority=1,
                action=self._update_drone_and_reschedule,
                event_type='DRONE_UPDATE',
                data={'drone_id': drone_id}
            )
            self.scheduler.schedule_event(next_event)

    def run(self):
        """
        Runs the event-driven simulation.
        """
        print("--- Starting Event-Driven Simulation ---")
        self.start_time_real = time.time()
        
        self._setup_initial_events()

        while not self.scheduler.is_empty():
            event = self.scheduler.get_next_event()
            
            # Print status periodically
            # We can make this more sophisticated later
            current_sim_time = self.scheduler.current_time
            if int(current_sim_time) % 10 == 0 and abs(current_sim_time - int(current_sim_time)) < self.time_step:
                 # This is a simple way to print roughly every 10 seconds of sim time
                 drone = list(self.drones.values())[0] # For single drone sim
                 # print(f"  > Sim Time: {current_sim_time:.2f}s, Drone Pos: {drone.pos}, Bat: {drone.battery_level:.2f}%")


            # Execute the event's action
            if event.action:
                # The data for our event is a dictionary, so we pass it as keyword arguments
                event.action(**event.data)

        end_time_real = time.time()
        print("\n--- Simulation Finished: No more events in the queue ---")
        print(f"Total Real Time Elapsed: {end_time_real - self.start_time_real:.2f} seconds")
        
        self.print_summary()

    def print_summary(self):
        """Prints a summary of the simulation results."""
        print("\n--- Mission Summary ---")
        for drone_id, drone in self.drones.items():
            print(f"Drone ID: {drone_id}")
            print(f"  Total Mission Time: {self.scheduler.current_time:.2f} seconds")
            print(f"  Final Drone Status: {drone.status}")
            print(f"  Final Position: {drone.pos}")
            print(f"  Remaining Battery: {drone.battery_level:.2f}%")
