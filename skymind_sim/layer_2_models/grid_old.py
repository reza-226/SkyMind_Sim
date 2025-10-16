# path: skymind_sim/layer_1_simulation/world/grid.py

import json
from skymind_sim.utils.log_manager import LogManager

class Grid:
    """Manages the grid, including dimensions, obstacles, and map loading."""
    
    # این تابع __init__ پارامتر map_path را می‌پذیرد.
    # این همان چیزی است که برای رفع خطا لازم است.
    def __init__(self, map_path: str):
        self.logger = LogManager.get_logger(__name__)
        
        # Initialize with default values first
        self.map_data = {}
        self.width = 20
        self.height = 20
        self.cell_size = 30
        self.obstacles = []

        if map_path:
            self._load_map(map_path)
        else:
            self.logger.warning("No map path provided. Using default 20x20 empty grid.")

    def _load_map(self, map_path: str):
        """Loads map data from a JSON file."""
        try:
            with open(map_path, 'r') as f:
                data = json.load(f)

            # Validate and assign grid properties
            self.width = data['width']
            self.height = data['height']
            self.cell_size = data.get('cell_size', self.cell_size)
            self.obstacles = [tuple(obs) for obs in data.get('obstacles', [])]
            
            # Store the raw data for other modules to use (e.g., for loading drones)
            self.map_data = data

            self.logger.info(f"Successfully loaded map '{map_path}'. Dimensions: {self.width}x{self.height}")

        except FileNotFoundError:
            self.logger.error(f"Map file not found at '{map_path}'.")
            self.logger.warning(f"Using default {self.width}x{self.height} grid.")
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON format in map file: '{map_path}'.")
            self.logger.warning(f"Using default {self.width}x{self.height} grid.")
        except KeyError as e:
            self.logger.error(f"Map file '{map_path}' is missing a required key: {e}.")
            self.logger.warning(f"Using default {self.width}x{self.height} grid.")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred loading map '{map_path}': {e}")
            self.logger.warning(f"Using default {self.width}x{self.height} grid.")

    def is_obstacle(self, x: int, y: int) -> bool:
        """Checks if a given cell is an obstacle."""
        return (x, y) in self.obstacles

    def is_within_bounds(self, x: int, y: int) -> bool:
        """Checks if a given coordinate is within the grid boundaries."""
        return 0 <= x < self.width and 0 <= y < self.height
