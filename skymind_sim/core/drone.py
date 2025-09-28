# skymind_sim/core/drone.py

import logging

logger = logging.getLogger(__name__)

class Drone:
    """
    Represents a single drone in the simulation.
    Manages its own state, position, and pathfinding.
    """
    def __init__(self, drone_id, start_pos, goal_pos, environment):
        """
        Initializes a Drone instance.

        Args:
            drone_id (str): A unique identifier for the drone (e.g., 'A').
            start_pos (tuple): The starting (row, col) coordinates.
            goal_pos (tuple): The goal (row, col) coordinates.
            environment (Environment): A reference to the simulation environment.
        """
        self.drone_id = drone_id
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.environment = environment  # Store a reference to the environment

        # --- Drone State ---
        self.current_pos = start_pos
        self.path = []  # The calculated path to the goal
        self.status = "IDLE"  # Can be IDLE, MOVING, FINISHED, FAILED

        logger.info(
            f"Drone {self.drone_id} initialized. Start: {self.start_pos}, "
            f"Goal: {self.goal_pos}, Status: {self.status}"
        )

    def calculate_path(self):
        """
        Calculates the path from the current position to the goal.
        (This will be implemented with an algorithm like A* later).
        """
        logger.info(f"Drone {self.drone_id}: Calculating path (placeholder)...")
        # For now, we'll use a placeholder path.
        # In a real scenario, this would involve a complex algorithm.
        self.path = [self.start_pos, self.goal_pos] # Simple straight line for now
        self.status = "READY"
        logger.info(f"Drone {self.drone_id}: Path calculated. Status set to {self.status}.")

    def move(self):
        """
        Moves the drone one step along its calculated path.
        """
        if self.status not in ["READY", "MOVING"]:
            logger.warning(f"Drone {self.drone_id} cannot move in status {self.status}.")
            return

        if not self.path:
            logger.info(f"Drone {self.drone_id} has reached its destination.")
            self.status = "FINISHED"
            return

        # Move to the next point in the path
        # In a real simulation, we'd pop the *next* step, not the start.
        # For now, let's just simulate the process.
        if self.current_pos == self.start_pos: # First move
            self.status = "MOVING"

        next_pos = self.path.pop(0)
        self.current_pos = next_pos
        logger.info(f"Drone {self.drone_id} moved to {self.current_pos}.")

        if not self.path:
            logger.info(f"Drone {self.drone_id} has reached its destination {self.goal_pos}.")
            self.status = "FINISHED"

    def __repr__(self):
        return (f"Drone(ID='{self.drone_id}', Pos={self.current_pos}, "
                f"Status='{self.status}')")
