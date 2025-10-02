# skymind_sim/layer_1_simulation/simulation.py

from typing import List
from .scheduler import Scheduler
from .entities.drone import Drone
from .world.obstacle import Obstacle

class Simulation:
    """
    The main orchestrator for the simulation logic (Layer 1).
    It holds the state of the world, including all entities, and manages the main simulation loop.
    It does NOT know about Pygame, rendering, or AI algorithms directly.
    """
    def __init__(self):
        print("Initializing Simulation (Layer 1)...")
        self.scheduler = Scheduler()
        self.drones: List[Drone] = []
        self.obstacles: List[Obstacle] = []
        self.is_running = False

    def setup_world(self):
        """
        Initializes the simulation world with drones and obstacles.
        In a real scenario, this would load from a config file or map.
        """
        print("Setting up simulation world...")
        # Create a sample drone
        drone1 = Drone(drone_id=1, position=(50, 50))
        self.drones.append(drone1)

        # Create a sample obstacle
        obstacle1 = Obstacle(obstacle_id=101, position=(200, 150), size=(100, 50))
        self.obstacles.append(obstacle1)
        print("World setup complete.")

    def start(self):
        """Starts the simulation loop."""
        print("Simulation started.")
        self.is_running = True

    def stop(self):
        """Stops the simulation loop."""
        print("Simulation stopped.")
        self.is_running = False

    def update(self, dt: float):
        """
        The main update loop of the simulation.
        This method is called repeatedly to advance the state of the world.

        Args:
            dt (float): The time elapsed since the last update.
        """
        if not self.is_running:
            return

        # 1. Advance the simulation time
        self.scheduler.tick(dt)

        # 2. Update all entities
        # In a real simulation, AI (Layer 3) would provide movement commands.
        # For now, let's just move the first drone slightly.
        if self.drones:
            drone = self.drones[0]
            # Simple hardcoded movement for demonstration
            drone.move(dx=1.0, dy=0.5)

        # 3. Perform other logic (e.g., collision detection) in the future

    def get_world_state(self) -> dict:
        """
        Provides the complete state of the simulation world.
        This is the primary method for Layer 0 (Presentation) to get data for rendering.
        """
        return {
            'drones': [d.get_state() for d in self.drones],
            'obstacles': [o.get_state() for o in self.obstacles],
            'time': self.scheduler.get_time(),
        }
