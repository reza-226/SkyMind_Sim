# skymind_sim/core/simulation.py

import logging
import time

from skymind_sim.core.drone import Drone

logger = logging.getLogger(__name__)

class Simulation:
    """
    Manages the main simulation loop and the interaction between drones and the environment.
    """
    def __init__(self, environment):
        """
        Initializes the Simulation.

        Args:
            environment (Environment): The simulation environment, containing the map and drone start/goal points.
        """
        self.environment = environment
        self.drones = []
        self.time_step = 0
        self.max_steps = 100  # A safety limit to prevent infinite loops

        self._initialize_drones()

    def _initialize_drones(self):
        """
        Creates Drone objects based on the data from the environment.
        """
        logger.info("Initializing drones...")
        # This code is now guaranteed to work with the updated Environment class
        for drone_def in self.environment.drone_definitions:
            drone = Drone(
                drone_id=drone_def['id'],
                start_pos=drone_def['start'],
                goal_pos=drone_def['goal'],
                environment=self.environment
            )
            self.drones.append(drone)
            logger.info(
                f"Initialized Drone '{drone_def['id']}' with start {drone_def['start']} and goal {drone_def['goal']}."
            )

    def run(self):
        """
        Runs the main simulation loop.
        """
        logger.info(f"Starting simulation run for {len(self.drones)} drones.")

        # --- 1. Path Calculation Phase ---
        logger.info("=== Phase 1: Path Calculation ===")
        for drone in self.drones:
            drone.calculate_path()
        logger.info("All drone paths calculated.")

        # --- 2. Movement Phase ---
        logger.info("=== Phase 2: Coordinated Movement ===")
        while self.time_step < self.max_steps:
            logger.info(f"--- Time Step: {self.time_step} ---")

            if all(d.status == "FINISHED" for d in self.drones):
                logger.info("All drones have reached their destinations. Simulation successful.")
                break

            for drone in self.drones:
                if drone.status != "FINISHED":
                    logger.info(f"--- Simulating movement for Drone '{drone.drone_id}' ---")
                    drone.move()

            self.time_step += 1
            time.sleep(0.1)

        if self.time_step >= self.max_steps:
            logger.warning("Simulation reached max steps limit. Ending.")

        logger.info("Simulation run finished.")

    def get_results(self):
        """
        Returns the final state of the simulation.
        """
        return {
            "total_time_steps": self.time_step,
            "drones": [
                {
                    "id": d.drone_id,
                    "status": d.status,
                    "final_position": d.current_pos
                }
                for d in self.drones
            ]
        }
