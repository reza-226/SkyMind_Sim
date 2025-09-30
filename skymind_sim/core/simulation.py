# skymind_sim/core/simulation.py

import time

class Simulation:
    """
    Manages the execution of the drone flight simulation.
    """
    def __init__(self, environment, drone, path):
        """
        Initializes the simulation.

        Args:
            environment (Environment): The simulation environment.
            drone (Drone): The drone instance to be simulated.
            path (list): The list of coordinates for the drone to follow.
        """
        self.env = environment
        self.drone = drone
        self.path = path
        # It's good practice to also inform the drone object about its path
        if hasattr(self.drone, 'set_path'):
            self.drone.set_path(path)

    def run(self, time_step=0.5):
        """
        Runs the text-based simulation step by step.
        """
        if not self.path:
            print("Simulation cannot run: No path provided.")
            return

        # The print statement is now moved to main.py to avoid confusion
        self.drone.status = "flying"
        
        # The first point in the path is the start point. We iterate from the second point.
        for point in self.path[1:]:
            if hasattr(self.drone, 'update_position'):
                self.drone.update_position(point)
            else:
                # Fallback if drone doesn't have this method yet
                self.drone.position = point
                print(f"Drone position updated to: {self.drone.position}")
            
            print(f"Drone at {self.drone.position}, Battery: {self.drone.battery_level:.1f}%")
            time.sleep(time_step) # Pause to make the simulation readable

        self.drone.status = "landed"
        print("--- Simulation Finished ---")
        print(f"Drone has reached the destination: {self.drone.position}")
        print(f"Final Status: {self.drone.status}")

    def get_results(self):
        """
        Returns a summary of the simulation results.
        """
        return {
            "final_position": self.drone.position,
            "final_status": self.drone.status,
            "total_steps": len(self.path) if self.path else 0
        }
