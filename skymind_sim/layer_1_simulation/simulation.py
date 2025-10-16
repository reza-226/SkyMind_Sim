# skymind_sim/layer_1_simulation/simulation.py

import json
from skymind_sim.utils.log_manager import LogManager
from skymind_sim.layer_1_simulation.world.grid import Grid
from skymind_sim.layer_1_simulation.entities.drone import Drone

class Simulation:
    """
    Manages the overall simulation state, including the grid, drones, and time.
    """
    def __init__(self, map_file_path: str):
        """
        Initializes the simulation by loading a map and setting up the environment.

        Args:
            map_file_path (str): The path to the JSON file describing the map.
        """
        self.logger = LogManager.get_logger(__name__)
        self.logger.info(f"Initializing simulation with map from: '{map_file_path}'")
        
        self.grid = None
        self.drones = []
        self.current_time = 0.0
        
        self._load_map(map_file_path)
        
        self.logger.info(f"Simulation successfully initialized with map: '{map_file_path}'")

    def _load_map(self, file_path: str):
        """
        Loads the map data from a JSON file to initialize the grid, obstacles, and drones.
        This method is robust to handle position data as both a dictionary {'x': val, 'y': val}
        and a list [val, val]. It also correctly handles the drones section whether it is a 
        list of objects or a dictionary of objects.
        """
        try:
            with open(file_path, 'r') as f:
                map_data = json.load(f)

            # Initialize Grid
            grid_size = map_data['grid_size']
            self.grid = Grid(width=grid_size['width'], height=grid_size['height'])
            self.logger.info(f"Grid created with dimensions {grid_size['width']}x{grid_size['height']}.")

            # Add Obstacles
            obstacle_count = 0
            if 'obstacles' in map_data:
                for obstacle_data in map_data['obstacles']:
                    pos = obstacle_data['position']
                    if isinstance(pos, dict):
                        obstacle_pos = (int(pos['x']), int(pos['y']))
                    elif isinstance(pos, list) and len(pos) == 2:
                        obstacle_pos = (int(pos[0]), int(pos[1]))
                    else:
                        self.logger.warning(f"Skipping obstacle with malformed position data: {pos}")
                        continue
                    
                    self.grid.add_obstacle(obstacle_pos)
                    obstacle_count += 1
            self.logger.info(f"Added {obstacle_count} obstacles to the grid.")

            # Initialize Drones
            drone_count = 0
            if 'drones' in map_data:
                drones_section = map_data['drones']
                
                # Check if drones_section is a dictionary (like {"D1": ..., "D2": ...})
                if isinstance(drones_section, dict):
                    # Iterate over key-value pairs (e.g., 'D1', {'start_position': [1,1]})
                    for drone_id, drone_info in drones_section.items():
                        start_pos_data = drone_info['start_position']
                        
                        if isinstance(start_pos_data, dict):
                            start_pos = (int(start_pos_data['x']), int(start_pos_data['y']))
                        elif isinstance(start_pos_data, list) and len(start_pos_data) == 2:
                            start_pos = (int(start_pos_data[0]), int(start_pos_data[1]))
                        else:
                            self.logger.warning(f"Skipping drone '{drone_id}' with malformed start_position: {start_pos_data}")
                            continue
                            
                        drone = Drone(drone_id=drone_id, start_position=start_pos)
                        self.drones.append(drone)
                        drone_count += 1
                
                # Check if drones_section is a list (like [{"id": "D1", ...}])
                elif isinstance(drones_section, list):
                    for drone_data in drones_section:
                        drone_id = drone_data['id']
                        start_pos_data = drone_data['start_position']

                        if isinstance(start_pos_data, dict):
                            start_pos = (int(start_pos_data['x']), int(start_pos_data['y']))
                        elif isinstance(start_pos_data, list) and len(start_pos_data) == 2:
                            start_pos = (int(start_pos_data[0]), int(start_pos_data[1]))
                        else:
                            self.logger.warning(f"Skipping drone '{drone_id}' with malformed start_position: {start_pos_data}")
                            continue
                        
                        drone = Drone(drone_id=drone_id, start_position=start_pos)
                        self.drones.append(drone)
                        drone_count += 1

            self.logger.info(f"Initialized {drone_count} drones.")

        except FileNotFoundError:
            self.logger.error(f"Map file not found at: {file_path}")
            raise
        except json.JSONDecodeError:
            self.logger.error(f"Error decoding JSON from map file: {file_path}")
            raise
        except (KeyError, IndexError) as e:
            self.logger.error(f"Missing or malformed key/index in map file {file_path}: {e}")
            raise

    def get_grid(self) -> Grid:
        """Returns the simulation grid."""
        return self.grid

    def get_drones(self) -> list[Drone]:
        """Returns the list of drones in the simulation."""
        return self.drones

    def get_current_time(self) -> float:
        """Returns the current simulation time in seconds."""
        return self.current_time

    def update(self, delta_time: float):
        """
        Update the state of all simulation entities.
        
        Args:
            delta_time (float): The time elapsed since the last update in seconds.
        """
        grid_dims = self.grid.get_dimensions()
        for drone in self.drones:
            # --- START OF CHANGE ---
            # grid_dims is a tuple (width, height), so we access it with indices.
            drone.update(delta_time, grid_dims[0], grid_dims[1])
