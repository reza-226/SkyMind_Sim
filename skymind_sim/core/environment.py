# skymind_sim/core/environment.py

import logging

logger = logging.getLogger(__name__)

class Environment:
    """
    Represents the simulation environment, including the map and drone positions.
    """
    def __init__(self, map_file_path):
        """
        Initializes the environment by loading a map file.

        Args:
            map_file_path (str): The path to the map file.
        """
        self.map_file_path = map_file_path
        self.grid = []
        self.width = 0
        self.height = 0
        # This will be a LIST of dictionaries, e.g., [{'id':'A', 'start':(y,x), 'goal':(y,x)}, ...]
        self.drone_definitions = []
        
        self._load_map()

    def _load_map(self):
        """
        Loads the map from the file, parses it, and finds drone start/goal points.
        """
        logger.info(f"Attempting to load map from {self.map_file_path}")
        try:
            with open(self.map_file_path, 'r') as f:
                lines = [line.rstrip('\n') for line in f.readlines()]

            if not lines:
                raise ValueError("Map file is empty.")

            # Set dimensions and validate map consistency
            self.height = len(lines)
            self.width = len(lines[0])
            self.grid = [list(line) for line in lines]

            for i, line in enumerate(lines):
                if len(line) != self.width:
                    raise ValueError(f"Map line length mismatch. Line {i+1} has length {len(line)}, expected {self.width}.")

            logger.info(f"Map loaded successfully. Dimensions: {self.height}x{self.width}")

            # Find drone start and goal positions
            drone_locations = {}  # Temporary dict to pair up start/goal points
            for y, row in enumerate(self.grid):
                for x, char in enumerate(row):
                    if 'a' <= char <= 'z': # Start position
                        drone_id = char.upper()
                        if drone_id not in drone_locations:
                            drone_locations[drone_id] = {}
                        drone_locations[drone_id]['start'] = (y, x)
                    elif 'A' <= char <= 'Z': # Goal position
                        drone_id = char
                        if drone_id not in drone_locations:
                            drone_locations[drone_id] = {}
                        drone_locations[drone_id]['goal'] = (y, x)

            # Populate the final drone_definitions list
            for drone_id, positions in sorted(drone_locations.items()):
                if 'start' in positions and 'goal' in positions:
                    self.drone_definitions.append({
                        'id': drone_id,
                        'start': positions['start'],
                        'goal': positions['goal']
                    })
                    logger.info(f"Found drone pair '{drone_id}': start at {positions['start']}, goal at {positions['goal']}")

        except FileNotFoundError:
            logger.error(f"Map file not found at: {self.map_file_path}")
            raise
        except ValueError as e:
            logger.error(f"Error processing map file: {e}")
            raise

    def is_obstacle(self, y, x):
        """
        Checks if a given coordinate is an obstacle.
        """
        if not (0 <= y < self.height and 0 <= x < self.width):
            return True  # Out of bounds is treated as an obstacle
        return self.grid[y][x] == '#'
