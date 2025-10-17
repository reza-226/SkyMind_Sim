# skymind_sim/layer_1_simulation/world/grid.py

import pygame
import logging
from typing import Tuple

from skymind_sim.utils.config_loader import ConfigLoader

class Grid:
    """
    Represents the logical and visual grid of the simulation world.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        grid_config = ConfigLoader.get('grid')
        self.width = grid_config.get('width_in_cells', 50)  # World width in grid cells
        self.height = grid_config.get('height_in_cells', 40) # World height in grid cells
        cell_w = grid_config.get('cell_width_pixels', 30)
        cell_h = grid_config.get('cell_height_pixels', 30)
        self.cell_size = (cell_w, cell_h)
        self.grid_line_color = tuple(grid_config.get('line_color', [40, 40, 40]))
        
        # Calculate total world size in pixels
        self.world_width_pixels = self.width * self.cell_size[0]
        self.world_height_pixels = self.height * self.cell_size[1]

        self.logger.info(f"Grid initialized with dimensions {self.width}x{self.height} and cell size {self.cell_size}.")

    def get_world_size_in_cells(self) -> Tuple[int, int]:
        """Returns the grid dimensions in number of cells."""
        return self.width, self.height

    def get_world_size_in_pixels(self) -> Tuple[int, int]:
        """Returns the total world size in pixels."""
        return self.world_width_pixels, self.world_height_pixels

    def grid_to_pixel(self, grid_pos: tuple) -> tuple[float, float]:
        """
        Converts grid coordinates (e.g., [5, 10]) to pixel coordinates.
        This is the new name for the method.
        """
        px = grid_pos[0] * self.cell_size[0]
        py = grid_pos[1] * self.cell_size[1]
        return px, py

    def pixel_to_grid(self, pixel_pos: tuple) -> tuple[int, int]:
        """
        Converts pixel coordinates to grid cell coordinates.
        Renamed for consistency.
        """
        gx = int(pixel_pos[0] // self.cell_size[0])
        gy = int(pixel_pos[1] // self.cell_size[1])
        return gx, gy
        
    def draw(self, surface: pygame.Surface, camera_offset: pygame.math.Vector2):
        """
        Draws the grid lines on the given surface, adjusted by the camera offset.
        
        Args:
            surface (pygame.Surface): The Pygame surface to draw on.
            camera_offset (pygame.math.Vector2): The offset of the camera view.
        """
        # We only need to draw the lines that are visible on the screen.
        screen_rect = surface.get_rect()
        
        # Horizontal lines
        for y in range(self.height + 1):
            y_pos = y * self.cell_size[1] - camera_offset.y
            
            # Simple culling: only draw if the line is on screen
            if y_pos >= screen_rect.top and y_pos <= screen_rect.bottom:
                start_pos = (0 - camera_offset.x, y_pos)
                end_pos = (self.world_width_pixels - camera_offset.x, y_pos)
                pygame.draw.line(surface, self.grid_line_color, start_pos, end_pos)

        # Vertical lines
        for x in range(self.width + 1):
            x_pos = x * self.cell_size[0] - camera_offset.x
            
            # Simple culling
            if x_pos >= screen_rect.left and x_pos <= screen_rect.right:
                start_pos = (x_pos, 0 - camera_offset.y)
                end_pos = (x_pos, self.world_height_pixels - camera_offset.y)
                pygame.draw.line(surface, self.grid_line_color, start_pos, end_pos)
