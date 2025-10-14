# مسیر: skymind_sim/layer_2_models/grid.py

import json
from typing import List, Tuple, Optional, Any, Set
from typing_extensions import TypeAlias

Cell: TypeAlias = Tuple[int, int]

class Grid:
    def __init__(self, map_filename: str, logger: Optional[Any] = None):
        """
        Initializes the grid model, loads map data, and defines grid properties.
        """
        self.logger = logger
        self.width = 0
        self.height = 0
        self.start: Cell = (0, 0)
        self.goals: List[Cell] = []
        self.obstacles: Set[Cell] = set()
        
        # این مشخصه برای هماهنگی با Renderer اضافه شده است
        self.cell_size = 25

        try:
            self.load_from_json(map_filename)
            self.log(f"Grid loaded successfully from '{map_filename}'.", "info")
        except Exception as e:
            self.log(f"Failed to load map from '{map_filename}': {e}", "error")
            # Fallback to a default empty grid
            self.width = 20
            self.height = 20
            self.log("Initialized with a default 20x20 grid due to loading error.", "warning")

    def log(self, message: str, level: str = "info"):
        """Logs messages using the provided logger."""
        if self.logger:
            log_func = getattr(self.logger, level, self.logger.info)
            log_func(message)
        else:
            print(f"GRID_{level.upper()}: {message}")

    def load_from_json(self, filename: str):
        """Loads grid configuration from a JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.width = data["width"]
        self.height = data["height"]
        self.start = tuple(data["start"])
        self.goals = [tuple(g) for g in data["goals"]]
        self.obstacles = {tuple(obs) for obs in data["obstacles"]}

    def is_obstacle(self, cell: Cell) -> bool:
        """Checks if a given cell is an obstacle."""
        return cell in self.obstacles

    def is_within_bounds(self, cell: Cell) -> bool:
        """Checks if a given cell is within the grid boundaries."""
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height

    def get_neighbors(self, cell: Cell) -> List[Cell]:
        """Gets valid, walkable neighbor cells."""
        x, y = cell
        neighbors: List[Cell] = []
        potential_neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for neighbor in potential_neighbors:
            if self.is_within_bounds(neighbor) and not self.is_obstacle(neighbor):
                neighbors.append(neighbor)
        return neighbors
