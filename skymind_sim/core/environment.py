# skymind_sim/core/environment.py

import json

class Environment:
    """
    Represents the 3D environment for the simulation, including dimensions and obstacles.
    """
    # --- تغییر ۱: تغییر در __init__ ---
    def __init__(self, map_file):
        """
        Initializes the environment by loading a map from a JSON file.

        Args:
            map_file (str): The path to the JSON file containing the map data.
        """
        self.width = 0
        self.depth = 0
        self.height = 0
        self.obstacles = set()
        self._load_map(map_file)

    # --- تغییر ۲: تغییر نام متد به _load_map ---
    # این یک قرارداد خوب است که متدهای داخلی (که فقط توسط خود کلاس استفاده می‌شوند) با آندرلاین شروع شوند.
    def _load_map(self, map_file):
        """
        Loads the map dimensions and obstacles from a specified JSON file.
        
        Args:
            map_file (str): The path to the map file.
        """
        print(f"Loading map from: {map_file}")
        try:
            with open(map_file, 'r') as f:
                map_data = json.load(f)
            
            # Load dimensions
            dims = map_data.get("dimensions", {})
            self.width = dims.get("width", 100)
            self.depth = dims.get("depth", 100)
            self.height = dims.get("height", 50)

            # Load obstacles and add them to the set
            # The obstacles are stored as tuples for efficient lookup in the set
            obstacle_list = map_data.get("obstacles", [])
            self.obstacles = {tuple(obs) for obs in obstacle_list}
            
            print("Map loaded successfully.")
            
        except FileNotFoundError:
            print(f"Error: Map file not found at '{map_file}'. Using default empty environment.")
            # Set default dimensions if file not found
            self.width, self.depth, self.height = 100, 100, 50
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{map_file}'. Using default empty environment.")
            # Set default dimensions if JSON is invalid
            self.width, self.depth, self.height = 100, 100, 50


    def get_dimensions(self):
        """Returns the dimensions of the environment as a tuple (width, depth, height)."""
        return (self.width, self.depth, self.height)

    def is_obstacle(self, x, y, z):
        """
        Checks if a given coordinate is an obstacle.

        Returns:
            bool: True if the coordinate is an obstacle, False otherwise.
        """
        return (x, y, z) in self.obstacles
        
    def get_obstacles(self):
        """
        Returns the set of all obstacle coordinates.

        Returns:
            set: A set of tuples, where each tuple is an (x, y, z) obstacle coordinate.
        """
        return self.obstacles
