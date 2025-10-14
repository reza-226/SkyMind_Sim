# FILE: skymind_sim/layer_1_simulation/entities/drone.py

import logging
import random
from typing import TYPE_CHECKING

from skymind_sim.config import Config
if TYPE_CHECKING:
    from skymind_sim.layer_1_simulation.world.grid import Grid

class Drone:
    def __init__(self, id: str, x: int, y: int, config: Config, grid: 'Grid'):
        self.id = id
        self.x = x
        self.y = y
        self.config = config
        self.grid = grid
        
        self.logger = logging.getLogger(f"Drone.{self.id}")
        
        try:
            fps = self.config.getint('renderer', 'fps')
            speed = self.config.getfloat('drone_properties', 'speed') 
            
            if speed <= 0:
                self.logger.warning(f"Drone speed ({speed}) must be positive. Defaulting to 1.0.")
                speed = 1.0
            
            # Cooldown is the number of frames to wait for one move.
            # A speed of 1 cell/sec at 30 fps means moving every 30 frames.
            # A speed of 30 cells/sec at 30 fps means moving every 1 frame.
            self.move_cooldown = max(1, round(fps / speed)) 
            self.move_timer = 0
            
            self.logger.info(
                f"Drone '{self.id}' created at ({self.x}, {self.y}). "
                f"Move cooldown set to {self.move_cooldown} frames (for speed {speed} cells/sec at {fps} FPS)."
            )
            
        except (KeyError, ValueError) as e:
            self.logger.error(f"Error reading drone properties from config: {e}. Using default values.")
            self.move_cooldown = 5  # Default cooldown if config fails
            self.move_timer = 0

    def step(self):
        self.move_timer += 1
        if self.move_timer < self.move_cooldown:
            return 
        
        # Reset timer and attempt to move
        self.move_timer = 0
        possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        move_x, move_y = random.choice(possible_moves)
        
        new_x = self.x + move_x
        new_y = self.y + move_y

        # Check for obstacles and grid boundaries before moving
        if not self.grid.is_obstacle(new_x, new_y):
            self.x = new_x
            self.y = new_y
            self.logger.debug(f"Moved to ({self.x}, {self.y})")
        else:
            self.logger.debug(f"Movement to ({new_x}, {new_y}) blocked. Position remains ({self.x}, {self.y}).")

    def __repr__(self) -> str:
        return f"Drone(id='{self.id}', x={self.x}, y={self.y})"
