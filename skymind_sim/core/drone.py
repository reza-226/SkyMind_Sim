# skymind_sim/core/drone.py

class Drone:
    """
    Represents the state and basic properties of a drone.
    """
    def __init__(self, initial_position=(0, 0, 0), battery_level=100.0, status="idle"):
        """
        Initializes the drone.

        Args:
            initial_position (tuple, optional): The starting (x, y, z) position of the drone. 
                                                  Defaults to (0, 0, 0).
            battery_level (float, optional): The initial battery percentage. Defaults to 100.0.
            status (str, optional): The initial status of the drone. Defaults to "idle".
        """
        self.position = initial_position
        self.battery_level = battery_level
        self.status = status
        self.path = []

    def update_position(self, new_position):
        """Updates the drone's current position."""
        print(f"Drone moving from {self.position} to {new_position}")
        self.position = new_position
        # In a real simulation, we would consume battery here.
        # self.battery_level -= 0.1 

    def set_path(self, path):
        """Sets the calculated path for the drone to follow."""
        self.path = path
        print("Path set for the drone.")

    def get_status(self):
        """Returns a dictionary with the current state of the drone."""
        return {
            "position": self.position,
            "battery": self.battery_level,
            "status": self.status
        }

    def __str__(self):
        return (f"Drone at position {self.position} with {self.battery_level}% battery. "
                f"Status: {self.status}")
