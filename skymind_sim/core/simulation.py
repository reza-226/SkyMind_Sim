# skymind_sim/core/simulation.py

import time
import logging
import os

logger = logging.getLogger("simulation_log")

class Simulation:
    """
    Controls the main simulation loop and orchestrates the updates.
    """
    def __init__(self, environment, time_step=0.3):
        self.environment = environment
        self.time_step = time_step
        self.tick_count = 0
        self.running = False
        logger.info(f"Simulation initialized with a time step of {self.time_step}s.")

    def run(self):
        """
        Starts and runs the main simulation loop.
        """
        self.running = True
        logger.info("Simulation started.")
        
        try:
            while self.running:
                self.tick_count += 1
                logger.info(f"--- Simulation Tick {self.tick_count} ---")
                
                self._update()
                self._render()
                
                # Check for completion
                if self._all_drones_finished():
                    self.running = False
                    logger.info("All drones have completed their paths. Simulation finished.")
                
                time.sleep(self.time_step)

        except KeyboardInterrupt:
            logger.info("Simulation interrupted by user (Ctrl+C).")
            self.running = False
        except Exception as e:
            logger.critical(f"An unexpected critical error occurred: {e}", exc_info=True)
            print("\nA critical error occurred. The simulation has been aborted.")
            self.running = False

    def _update(self):
        """
        Updates the state of all drones in the environment.
        """
        if not self.environment.drones:
            logger.warning("No drones in the simulation to update.")
            self.running = False
            return
        
        # --- FIX: Iterate directly over the list of drones ---
        # The environment.drones is a list, not a dictionary.
        for drone in self.environment.drones:
            if not drone.has_finished():
                drone.move()

    def _render(self):
        """
        Renders the current state of the simulation to the console.
        """
        # Create a deep copy of the grid to draw on
        render_grid = [row[:] for row in self.environment.grid]
        
        # Draw drones on the grid
        for drone in self.environment.drones:
            r, c = drone.position
            # Ensure drone is within bounds before drawing
            if 0 <= r < self.environment.height and 0 <= c < self.environment.width:
                render_grid[r][c] = drone.char

        # Clear console and print the grid
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"SkyMind_Sim - Tick: {self.tick_count}")
        for row in render_grid:
            print("".join(row))
        
        # Print status of each drone
        print("\n--- Drone Status ---")
        for drone in self.environment.drones:
            status = "Finished" if drone.has_finished() else f"Moving (Path len: {len(drone.path)})"
            print(f"- {drone.id} at {drone.position}: {status}")
        print("--------------------")

    def _all_drones_finished(self):
        """
        Checks if all drones in the simulation have finished their paths.
        """
        if not self.environment.drones:
            return True # If there are no drones, we consider it "finished"
        
        return all(drone.has_finished() for drone in self.environment.drones)
