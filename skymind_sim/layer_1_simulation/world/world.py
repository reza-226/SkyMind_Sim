# skymind_sim/layer_1_simulation/world/world.py

import pygame
import logging
from typing import Dict, Optional

from skymind_sim.utils.config_loader import ConfigLoader
from skymind_sim.layer_1_simulation.world.grid import Grid
from skymind_sim.layer_1_simulation.entities.drone import Drone
# Assuming you might have other entities like Obstacle in the future
# from skymind_sim.layer_1_simulation.world.obstacle import Obstacle

class World:
    """
    Manages the simulation environment, including the grid and all entities within it.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing World...")

        # Initialize the grid
        self.grid = Grid()
        self.logger.info(f"Grid created with size: {self.grid.width}x{self.grid.height}")

        # Containers for entities
        self.drones: Dict[str, Drone] = {}
        # self.obstacles = []
        self.player_drone: Optional[Drone] = None

        self._initialize_entities()
        self.logger.info("World initialized successfully.")

    def _initialize_entities(self):
        """Initializes entities based on the world/map configuration."""
        self.logger.info("Initializing world entities...")
        
        # For now, we will hardcode the creation of one player drone.
        # Later, this can be driven by a map file.
        world_config = ConfigLoader.get('world')
        player_start_pos = world_config.get('player_start_position', [5, 5])
        
        # Create the player drone
        self.player_drone = Drone(
            drone_id="player_1",
            # --- THIS IS THE FIX ---
            position=player_start_pos,
            # -----------------------
            grid=self.grid
        )
        self.drones[self.player_drone.id] = self.player_drone
        self.logger.info(f"Player drone '{self.player_drone.id}' created at position {player_start_pos}.")

    def update(self, dt: float):
        """
        Updates the state of all entities in the world.
        
        Args:
            dt (float): The time elapsed since the last frame.
        """
        for drone in self.drones.values():
            drone.update(dt)

    def draw(self, surface: pygame.Surface, camera_offset: pygame.math.Vector2):
        """
        Draws all components of the world.
        
        Args:
            surface (pygame.Surface): The main display surface.
            camera_offset (pygame.math.Vector2): The camera's offset to adjust drawing positions.
        """
        # Draw the grid first as the background
        self.grid.draw(surface, camera_offset)

        # Draw all other entities
        for drone in self.drones.values():
            drone.draw(surface, camera_offset)

    def get_player_drone(self) -> Optional[Drone]:
        """Returns the main player-controlled drone."""
        return self.player_drone
