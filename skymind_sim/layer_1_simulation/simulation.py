# skymind_sim/layer_1_simulation/simulation.py

import json
import logging
from .entities.drone import Drone
from .world.obstacle import Obstacle

logger = logging.getLogger(__name__)

class Simulation:
    """
    Manages the simulation state, including all entities and the world environment.
    It's the heart of Layer 1.
    """
    def __init__(self):
        self.drones = {}
        self.obstacles = {}
        self.world_size = (800, 600)  # Default size, can be overridden by map file
        logger.info("Simulation (Layer 1) initialized.")

    def load_world_from_file(self, file_path: str):
        """
        Loads the simulation world configuration from a JSON file.
        """
        logger.info(f"Attempting to load world from: {file_path}")
        try:
            with open(file_path, 'r') as f:
                world_data = json.load(f)

            self.world_size = tuple(world_data.get("world_size", self.world_size))

            # Clear previous entities
            self.drones.clear()
            self.obstacles.clear()

            # Load drones
            for drone_info in world_data.get("drones", []):
                drone_id = drone_info["id"]
                pos = tuple(drone_info["start_position"])
                speed = drone_info.get("speed", 50) # Default speed if not specified
                self.drones[drone_id] = Drone(drone_id, initial_position=pos, speed=speed)

            # Load obstacles
            for obs_info in world_data.get("obstacles", []):
                obs_id = obs_info["id"]
                pos = tuple(obs_info["position"])
                size = tuple(obs_info["size"])
                self.obstacles[obs_id] = Obstacle(obs_id, position=pos, size=size)
            
            logger.info(f"World setup complete: {len(self.drones)} drone(s), {len(self.obstacles)} obstacle(s).")

        except FileNotFoundError:
            logger.error(f"Map file not found at: {file_path}")
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from file: {file_path}")
        except KeyError as e:
            logger.error(f"Missing key in map file {file_path}: {e}")

    def setup_test_world(self):
        """
        (DEPRECATED) Sets up a simple, hard-coded world for testing purposes.
        We will keep this for a while for quick tests but loading from file is preferred.
        """
        # Create a drone
        drone1 = Drone(drone_id="d1", initial_position=(100, 100), speed=100)
        self.drones[drone1.id] = drone1
        drone1.set_path([(700, 100), (700, 500), (100, 500), (100, 100)])

        # Create an obstacle
        obs1 = Obstacle(obstacle_id="obs1", position=(300, 200), size=(50, 150))
        self.obstacles[obs1.id] = obs1
        
        logger.info(f"Test world setup complete: {len(self.drones)} drone, {len(self.obstacles)} obstacle.")

    def update(self, dt: float):
        """
        Updates the state of all entities in the simulation.
        dt: delta time in seconds.
        """
        for drone in self.drones.values():
            drone.update(dt)

    def get_world_state(self) -> dict:
        """
        Returns a serializable dictionary representing the current state of the world.
        This is the primary way other layers get information from the simulation.
        """
        state = {
            "drones": [d.get_state() for d in self.drones.values()],
            "obstacles": [o.get_state() for o in self.obstacles.values()],
            "world_size": self.world_size
        }
        return state

    def set_drone_path(self, drone_id: str, path: list):
        """
        Sets the movement path for a specific drone.
        """
        if drone_id in self.drones:
            self.drones[drone_id].set_path(path)
            logger.info(f"Path set for drone '{drone_id}'.")
        else:
            logger.warning(f"Attempted to set path for non-existent drone '{drone_id}'.")
