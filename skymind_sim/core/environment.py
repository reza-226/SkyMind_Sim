# skymind_sim/core/environment.py

import logging
import heapq  # For the priority queue in A*

logger = logging.getLogger("simulation_log")

class Environment:
    """
    Manages the simulation grid, obstacles, and all drones.
    Responsible for pathfinding.
    """
    def __init__(self, map_file):
        self.grid = []
        self.width = 0
        self.height = 0
        self.drones = []
        try:
            self._load_map(map_file)
            logger.info(f"Environment initialized with map '{map_file}' ({self.height}x{self.width}).")
        except (ValueError, FileNotFoundError) as e:
            # The errors are already logged in _load_map. We just re-raise to halt execution.
            raise SystemExit(f"Halting due to critical error in map loading: {e}") from e

    def _load_map(self, map_file):
        """Loads the map from a text file."""
        try:
            with open(map_file, 'r') as f:
                lines = [line.strip('\n') for line in f.readlines()]

            if not lines:
                raise ValueError("Map file is empty.")

            # Validate that all lines have the same length
            self.width = len(lines[0])
            for i, line in enumerate(lines):
                if len(line) != self.width:
                    error_msg = f"Map line length mismatch. Expected {self.width}, but line {i+1} has {len(line)}."
                    logger.error(error_msg)
                    raise ValueError(error_msg)
            
            self.grid = [list(line) for line in lines]
            self.height = len(self.grid)
            logger.info(f"Map '{map_file}' loaded successfully.")

        except FileNotFoundError:
            logger.error(f"Map file not found at '{map_file}'")
            raise

    def add_drone(self, drone, end_pos):
        """Adds a drone to the environment and calculates its path."""
        logger.info(f"Adding drone '{drone.id}' to environment. Start: {drone.position}, End: {end_pos}")
        
        path = self._find_path(drone.position, end_pos)
        
        if path:
            drone.path = path
            self.drones.append(drone) # Only add the drone if a path is found
            logger.info(f"Path found for drone '{drone.id}' with {len(path)} steps. Drone added.")
        else:
            logger.warning(f"No path could be found for drone '{drone.id}' from {drone.position} to {end_pos}. Drone not added to simulation.")

    def _is_valid(self, pos):
        """Check if a position is within grid bounds and not an obstacle."""
        row, col = pos
        if not (0 <= row < self.height and 0 <= col < self.width):
            return False
        if self.grid[row][col] == '#':
            return False
        return True

    def _heuristic(self, a, b):
        """Manhattan distance heuristic for A*."""
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def _find_path(self, start, end):
        """
        Corrected A* pathfinding algorithm implementation.
        """
        if not self._is_valid(start) or not self._is_valid(end):
            logger.warning(f"Start {start} or End {end} is not a valid position.")
            return []

        open_set = []
        heapq.heappush(open_set, (0, start)) # (f_score, position)
        
        came_from = {}
        
        g_score = { (r, c): float('inf') for r in range(self.height) for c in range(self.width) }
        g_score[start] = 0
        
        f_score = { (r, c): float('inf') for r in range(self.height) for c in range(self.width) }
        f_score[start] = self._heuristic(start, end)

        open_set_hash = {start}

        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current == end:
                # Reconstruct path. The path is from start to end.
                # The returned path does not include the start position itself,
                # as the drone is already there. It contains the sequence of
                # cells to move to.
                path = []
                temp = current
                while temp in came_from:
                    path.append(temp)
                    temp = came_from[temp]
                path.reverse() # Path is now from start's neighbor to end
                return path

            open_set_hash.remove(current)

            row, col = current
            neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
            
            for neighbor in neighbors:
                if not self._is_valid(neighbor):
                    continue
                
                tentative_g_score = g_score[current] + 1
                
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self._heuristic(neighbor, end)
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)
        
        return [] # Return empty list if no path is found
