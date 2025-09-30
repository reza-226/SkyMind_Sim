# skymind_sim/core/environment.py

import json

class Environment:
    """
    Represents the physical environment of the simulation.
    Holds properties like dimensions and can load obstacles from a map file.
    """
    def __init__(self, width, height, map_file=None):
        """
        Initializes the Environment.

        If a map_file is provided, it loads data from it. Otherwise, it uses
        the provided width and height.

        Args:
            width (float): The default width of the simulation area if no map is loaded.
            height (float): The default height of the simulation area if no map is loaded.
            map_file (str, optional): The path to the map file (JSON). Defaults to None.
        """
        self.width = width
        self.height = height
        self.depth = 100  # Default depth, can be overwritten by map
        self.obstacles = set()

        if map_file:
            self._load_map(map_file)
        else:
            print(f"Environment initialized with default size ({self.width}x{self.height}). No map loaded.")

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
            
            # Load dimensions from map, overwriting defaults
            dims = map_data.get("dimensions", {})
            self.width = dims.get("width", self.width)
            self.depth = dims.get("depth", self.depth)
            self.height = dims.get("height", self.height)

            # Load obstacles and add them to the set
            # The obstacles are stored as tuples for efficient lookup in the set
            obstacle_list = map_data.get("obstacles", [])
            self.obstacles = {tuple(obs) for obs in obstacle_list}
            
            print("Map loaded successfully.")
            print(f"New environment dimensions: (Width: {self.width}, Depth: {self.depth}, Height: {self.height})")
            
        except FileNotFoundError:
            print(f"Error: Map file not found at '{map_file}'. Using default environment settings.")
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{map_file}'. Using default environment settings.")

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
