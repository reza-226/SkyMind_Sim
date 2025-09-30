import json
import numpy as np

class Environment:
    """
    Manages the 3D environment, including the map boundaries and obstacles.
    """
    def __init__(self, map_file_path):
        """
        Initializes the environment by loading a map file.

        Args:
            map_file_path (str): The path to the JSON map file.
        """
        try:
            print(f"Initializing Environment with map: {map_file_path}")
            self.map_data = self._load_map(map_file_path)

            # --- تغییرات اصلی اینجا شروع می‌شود ---

            # Extract bounds and cell size
            self.bounds_min = np.array(self.map_data['bounds']['min'])
            self.bounds_max = np.array(self.map_data['bounds']['max'])
            self.cell_size = self.map_data.get('grid_cell_size', 1.0)
            
            # Calculate grid dimensions
            grid_dims = np.ceil((self.bounds_max - self.bounds_min) / self.cell_size).astype(int)
            
            print(f"Environment created with grid dimensions: {tuple(grid_dims)}")

            # Create the grid and store it as a class attribute
            self.grid = np.zeros(tuple(grid_dims), dtype=np.int8)
            
            print("Populating obstacles in the grid...")
            self._populate_obstacles() # دیگر نیازی به ارسال grid به عنوان آرگومان نیست
            
            obstacle_count = len(self.map_data.get('obstacles', []))
            print(f"Finished populating {obstacle_count} obstacles.")
            
        except KeyError as e:
            raise Exception(f"An unexpected error occurred during environment loading: {e}")
        except Exception as e:
            raise Exception(f"Failed to initialize environment: {e}")

    def _load_map(self, file_path):
        """Loads map data from a JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _populate_obstacles(self):
        """Populates the grid with obstacles from the map data."""
        obstacles = self.map_data.get('obstacles', [])
        for obs in obstacles:
            if obs['type'] == 'box':
                min_corner = np.array(obs['min'])
                max_corner = np.array(obs['max'])
                
                # Convert world coordinates to grid indices
                start_idx = np.floor((min_corner - self.bounds_min) / self.cell_size).astype(int)
                end_idx = np.ceil((max_corner - self.bounds_min) / self.cell_size).astype(int)

                # Clip indices to be within grid bounds
                start_idx = np.maximum(start_idx, 0)
                end_idx = np.minimum(end_idx, self.grid.shape)

                # Mark the region as an obstacle (value 1)
                self.grid[start_idx[0]:end_idx[0], start_idx[1]:end_idx[1], start_idx[2]:end_idx[2]] = 1
