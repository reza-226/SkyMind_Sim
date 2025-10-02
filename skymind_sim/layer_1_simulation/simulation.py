# skymind_sim/layer_1_simulation/simulation.py

import json
import logging
from typing import Tuple, List, Optional
from .entities.drone import Drone
from .world.obstacle import Obstacle
# Import جدید برای PathPlanner
from skymind_sim.layer_3_intelligence.pathfinding.path_planner import PathPlanner

logger = logging.getLogger(__name__)

class Simulation:
    """
    Manages the simulation state, including all entities and the world environment.
    It's the heart of Layer 1 and now integrates with the pathfinding intelligence.
    """
    def __init__(self):
        self.drones = {}
        self.obstacles = {}
        self.world_size = (800, 600)
        # عضو جدید برای نگهداری برنامه‌ریز مسیر
        self.path_planner: Optional[PathPlanner] = None
        logger.info("Simulation (Layer 1) initialized.")

    def load_world_from_file(self, file_path: str):
        """
        Loads the simulation world configuration from a JSON file and initializes the PathPlanner.
        """
        logger.info(f"Attempting to load world from: {file_path}")
        try:
            with open(file_path, 'r') as f:
                world_data = json.load(f)

            self.world_size = tuple(world_data.get("world_size", self.world_size))

            self.drones.clear()
            self.obstacles.clear()

            # Load obstacles
            for obs_info in world_data.get("obstacles", []):
                obs_id = obs_info["id"]
                pos = tuple(obs_info["position"])
                size = tuple(obs_info["size"])
                self.obstacles[obs_id] = Obstacle(obs_id, position=pos, size=size)
            
            # --- بخش جدید: مقداردهی PathPlanner ---
            # پس از بارگذاری همه موانع، یک نمونه از PathPlanner می‌سازیم
            self.path_planner = PathPlanner(
                obstacles=list(self.obstacles.values()),
                world_bounds=self.world_size,
                grid_size=20  # اندازه گرید را می‌توان قابل تنظیم کرد
            )
            
            # Load drones
            for drone_info in world_data.get("drones", []):
                drone_id = drone_info["id"]
                pos = tuple(drone_info["start_position"])
                speed = drone_info.get("speed", 50)
                self.drones[drone_id] = Drone(drone_id, initial_position=pos, speed=speed)
                
                # --- بخش جدید: محاسبه مسیر هوشمند برای هر پهپاد ---
                # اگر نقطه هدف در فایل نقشه تعریف شده باشد، مسیر را محاسبه می‌کنیم
                if "target_position" in drone_info:
                    target_pos = tuple(drone_info["target_position"])
                    self.calculate_and_set_path(drone_id, pos, target_pos)

            logger.info(f"World setup complete: {len(self.drones)} drone(s), {len(self.obstacles)} obstacle(s).")

        except FileNotFoundError:
            logger.error(f"Map file not found at: {file_path}")
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from file: {file_path}")
        except KeyError as e:
            logger.error(f"Missing key in map file {file_path}: {e}")

    def setup_test_world(self):
        """
        Sets up a simple, hard-coded world for testing A* pathfinding.
        """
        # Create obstacles
        obs1 = Obstacle(obstacle_id="obs1", position=(200, 150), size=(50, 200))
        obs2 = Obstacle(obstacle_id="obs2", position=(400, 300), size=(200, 50))
        self.obstacles = {obs1.id: obs1, obs2.id: obs2}

        # مقداردهی PathPlanner با موانع
        self.path_planner = PathPlanner(
            obstacles=list(self.obstacles.values()),
            world_bounds=self.world_size,
            grid_size=20
        )

        # Create a drone and find a path for it
        start_pos = (50, 50)
        end_pos = (750, 550)
        drone1 = Drone(drone_id="d1", initial_position=start_pos, speed=150)
        self.drones[drone1.id] = drone1
        
        # محاسبه و تنظیم مسیر هوشمند
        self.calculate_and_set_path(drone1.id, start_pos, end_pos)
        
        logger.info(f"Test world setup complete with A* pathfinding.")

    def calculate_and_set_path(self, drone_id: str, start_pos: Tuple[int, int], end_pos: Tuple[int, int]):
        """
        Calculates a path using the PathPlanner and sets it for the specified drone.
        """
        if not self.path_planner:
            logger.error("PathPlanner is not initialized. Cannot find path.")
            return

        # پیدا کردن مسیر با استفاده از PathPlanner
        path = self.path_planner.find_path(start_pos, end_pos)
        
        if path:
            self.set_drone_path(drone_id, path)
        else:
            logger.warning(f"Could not find a path for drone '{drone_id}' from {start_pos} to {end_pos}.")

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
        """
        state = {
            "drones": [d.get_state() for d in self.drones.values()],
            "obstacles": [o.get_state() for o in self.obstacles.values()],
            "world_size": self.world_size
        }
        return state

    def set_drone_path(self, drone_id: str, path: List[Tuple[int, int]]):
        """
        Sets the movement path for a specific drone.
        """
        if drone_id in self.drones:
            self.drones[drone_id].set_path(path)
            logger.info(f"Path with {len(path)} waypoints set for drone '{drone_id}'.")
        else:
            logger.warning(f"Attempted to set path for non-existent drone '{drone_id}'.")
