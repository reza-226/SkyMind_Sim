# FILE: skymind_sim/core/environment.py

class Environment:
    """
    Manages the state of the simulation world, including all drones and static objects.
    """
    def __init__(self, width, height):
        """
        Initializes the environment.

        Args:
            width (int): The width of the simulation area.
            height (int): The height of the simulation area.
        """
        self.width = width
        self.height = height
        self.drones = []
        self.obstacles = []  # Future use: for static obstacles like buildings
        self.charging_stations = [] # Future use: for charging stations

    def add_drone(self, drone):
        """
        Adds a drone to the environment.

        Args:
            drone (Drone): The drone object to add.
        """
        if drone not in self.drones:
            self.drones.append(drone)
            # --- MODIFIED LINE ---
            print(f"Added drone to simulation: {drone.drone_id}")
            # --- END OF MODIFIED LINE ---

    def update_state(self, delta_time):
        """
        Updates the state of all objects in the environment for one time step.
        """
        for drone in self.drones:
            drone.update(delta_time)
            # Future logic: collision detection, boundary checks, etc.

    def get_all_drones(self):
        """
        Returns a list of all drones in the environment.
        """
        return self.drones