# skymind_sim/layer_1_simulation/scheduler.py

class Scheduler:
    """
    A simple time scheduler for the simulation.
    It manages the simulation time and ticks.
    Belongs to Layer 1 as it controls the flow of the simulation itself.
    """
    def __init__(self):
        self.time: float = 0.0
        self.tick_count: int = 0
        print("Scheduler initialized.")

    def tick(self, dt: float):
        """
        Advances the simulation time by a delta.

        Args:
            dt (float): The time step for this tick (e.g., 0.1 seconds).
        """
        self.time += dt
        self.tick_count += 1
        print(f"--- Simulation Tick {self.tick_count}: Time = {self.time:.2f}s ---")

    def get_time(self) -> float:
        return self.time
