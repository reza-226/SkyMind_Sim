# skymind_sim/core/drone.py

class Drone:
    """
    Represents a single drone in the simulation.
    """
    def __init__(self, drone_id: int, initial_position: tuple = (0, 0, 0)):
        """
        Initializes a new Drone.

        Args:
            drone_id (int): The unique identifier for the drone.
            initial_position (tuple): The starting (x, y, z) position of the drone.
        """
        if not isinstance(drone_id, int):
            raise TypeError("Drone ID must be an integer.")
        if not (isinstance(initial_position, tuple) and len(initial_position) == 3):
            raise ValueError("Initial position must be a tuple of (x, y, z).")

        self.id = drone_id
        self.position = initial_position
        self.velocity = (0, 0, 0)  # Starting with zero velocity
        self.status = 'IDLE'       # Initial status

    def __repr__(self) -> str:
        """
        Provides a developer-friendly string representation of the drone.
        """
        return (f"Drone(id={self.id}, position={self.position}, "
                f"status='{self.status}')")

    def move(self, new_position: tuple):
        """
        Updates the drone's position.
        In a real simulation, this would involve physics, but for now, we just teleport.
        """
        print(f"Drone {self.id}: Moving from {self.position} to {new_position}")
        self.position = new_position
        self.update_status('FLYING')

    def land(self):
        """
        Lands the drone, setting its status to IDLE.
        """
        print(f"Drone {self.id}: Landing at position {self.position}.")
        self.update_status('IDLE')

    def update_status(self, new_status: str):
        """
        Updates the drone's status.
        """
        print(f"Drone {self.id}: Status changed from '{self.status}' to '{new_status}'.")
        self.status = new_status
