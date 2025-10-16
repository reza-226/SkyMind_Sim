# skymind_sim/layer_0_presentation/renderer.py

import pygame
from typing import Tuple

from skymind_sim.layer_0_presentation.asset_loader import AssetLoader
from skymind_sim.layer_1_simulation.simulation import Simulation
from skymind_sim.utils.log_manager import LogManager

# Define some colors
COLOR_BACKGROUND = (25, 25, 35)
COLOR_GRID_LINES = (50, 50, 60)
COLOR_OBSTACLE = (100, 100, 110)
COLOR_TEXT = (220, 220, 220)

class Renderer:
    """Handles all drawing operations for the simulation."""

    def __init__(self, screen: pygame.Surface, asset_loader: AssetLoader, grid_dims: Tuple[int, int]):
        """
        Initializes the Renderer.
        Args:
            screen (pygame.Surface): The main display surface created with pygame.
            asset_loader (AssetLoader): The asset loader instance.
            grid_dims (Tuple[int, int]): The dimensions (width, height) of the simulation grid.
        """
        self.logger = LogManager.get_logger(__name__)
        
        # --- START OF CHANGES ---
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        # --- END OF CHANGES ---

        self.asset_loader = asset_loader
        self.grid_width, self.grid_height = grid_dims
        
        self.font_main = self.asset_loader.get_font('Roboto-Regular', 16)
        
        self.drone_image_original = self.asset_loader.get_image('drone_icon')
        
        self._calculate_cell_size()
        self.drone_image_scaled = None # Will be created after cell size is known
        self._scale_assets()
        
        self.logger.info("Renderer initialized successfully.")

    def _calculate_cell_size(self):
        """Calculate the optimal cell size to fit the grid in the window."""
        # Subtract some padding
        drawable_width = self.width * 0.9
        drawable_height = self.height * 0.9
        
        cell_w = drawable_width / self.grid_width
        cell_h = drawable_height / self.grid_height
        
        self.cell_size = int(min(cell_w, cell_h))
        
        self.grid_render_width = self.cell_size * self.grid_width
        self.grid_render_height = self.cell_size * self.grid_height
        
        # Center the grid
        self.grid_offset_x = (self.width - self.grid_render_width) // 2
        self.grid_offset_y = (self.height - self.grid_render_height) // 2
        
        self.logger.info(f"Calculated cell size: {self.cell_size}px")

    def _scale_assets(self):
        """Scale assets based on the calculated cell size."""
        if self.drone_image_original:
            image_size = int(self.cell_size * 0.8) # 80% of cell size
            self.drone_image_scaled = pygame.transform.scale(
                self.drone_image_original, (image_size, image_size)
            )
            self.logger.info(f"Scaled drone image to {image_size}x{image_size}px.")

    def render_all(self, simulation: Simulation):
        """Render the entire simulation state."""
        self.screen.fill(COLOR_BACKGROUND)
        self._draw_grid()
        self._draw_obstacles(simulation.get_grid())
        self._draw_drones(simulation)
        pygame.display.flip()

    def _draw_grid(self):
        """Draw the grid lines."""
        for x in range(self.grid_width + 1):
            start_pos = (self.grid_offset_x + x * self.cell_size, self.grid_offset_y)
            end_pos = (self.grid_offset_x + x * self.cell_size, self.grid_offset_y + self.grid_render_height)
            pygame.draw.line(self.screen, COLOR_GRID_LINES, start_pos, end_pos)

        for y in range(self.grid_height + 1):
            start_pos = (self.grid_offset_x, self.grid_offset_y + y * self.cell_size)
            end_pos = (self.grid_offset_x + self.grid_render_width, self.grid_offset_y + y * self.cell_size)
            pygame.draw.line(self.screen, COLOR_GRID_LINES, start_pos, end_pos)

    def _draw_obstacles(self, grid):
        """Draw the obstacles on the grid."""
        for obs in grid.get_obstacles():
            # --- START OF CHANGE ---
            # 'obs' is a tuple (x, y), so we use indices 0 and 1.
            rect = pygame.Rect(
                self.grid_offset_x + obs[0] * self.cell_size,
                self.grid_offset_y + obs[1] * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            # --- END OF CHANGE ---
            pygame.draw.rect(self.screen, COLOR_OBSTACLE, rect)
            
    def _draw_drones(self, simulation: Simulation):
        """Draw the drones on the grid."""
        if not self.drone_image_scaled:
            return

        for drone in simulation.get_drones():
            # Convert grid coordinates to pixel coordinates
            pixel_x = self.grid_offset_x + drone.position[0] * self.cell_size
            pixel_y = self.grid_offset_y + drone.position[1] * self.cell_size
            
            # Center the image in the cell
            offset = (self.cell_size - self.drone_image_scaled.get_width()) // 2
            
            self.screen.blit(self.drone_image_scaled, (pixel_x + offset, pixel_y + offset))

    def close(self):
        """Perform any cleanup."""
        # The main loop now handles pygame.quit()
        self.logger.info("Renderer closed.")
