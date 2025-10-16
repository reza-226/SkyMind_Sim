# In file: skymind_sim/layer_0_presentation/renderer.py

import pygame
from ..utils.log_manager import LogManager
from .asset_loader import AssetLoader

# --- Constants for Colors ---
COLOR_BACKGROUND = (240, 240, 240)  # Light gray
COLOR_GRID_LINES = (200, 200, 200)  # Lighter gray
COLOR_OBSTACLE = (80, 80, 80)        # Dark gray
COLOR_TEXT = (50, 50, 50)            # Dark text color

class Renderer:
    """
    Handles all rendering tasks for the simulation, including drawing the grid,
    drones, obstacles, and UI elements.
    """
    def __init__(self, screen, grid_dims, padding=20):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.grid_dims = grid_dims
        self.padding = padding
        self.logger = LogManager.get_logger(__name__)
        
        # Renderer now creates its own instance of AssetLoader
        self.assets = AssetLoader()

        # Get a font for rendering text. We assume 'Roboto-Regular' is loaded.
        try:
            self.font = self.assets.get_font('Roboto-Regular', 14) # Size 14
        except KeyError:
            self.logger.warning("Font 'Roboto-Regular' not found. Using Pygame's default font.")
            self.font = pygame.font.Font(None, 20) # A fallback default font

        self._calculate_grid_properties()
        self._prepare_assets()
        
        self.logger.info("Renderer initialized successfully.")

    def _calculate_grid_properties(self):
        """Calculates cell size and grid offsets based on screen dimensions."""
        drawable_width = self.screen_width - 2 * self.padding
        drawable_height = self.screen_height - 2 * self.padding

        # Calculate cell size based on the limiting dimension
        cell_w = drawable_width / self.grid_dims[0]
        cell_h = drawable_height / self.grid_dims[1]
        self.cell_size = int(min(cell_w, cell_h))

        self.grid_render_width = self.cell_size * self.grid_dims[0]
        self.grid_render_height = self.cell_size * self.grid_dims[1]

        self.grid_offset_x = (self.screen_width - self.grid_render_width) / 2
        self.grid_offset_y = (self.screen_height - self.grid_render_height) / 2
        
        self.logger.info(f"Calculated cell size: {self.cell_size}px")

    def _prepare_assets(self):
        """Prepares assets needed for rendering, like scaling images."""
        drone_icon_size = int(self.cell_size * 0.8)  # 80% of cell size
        self.drone_image = self.assets.get_image('drone_icon')
        if self.drone_image:
            self.drone_image = pygame.transform.scale(self.drone_image, (drone_icon_size, drone_icon_size))
            self.logger.info(f"Scaled drone image to {drone_icon_size}x{drone_icon_size}px.")

    def render_all(self, simulation):
        """Renders the entire simulation state."""
        self.screen.fill(COLOR_BACKGROUND)
        self._draw_grid()
        self._draw_obstacles(simulation.grid)
        self._draw_drones(simulation.drones)
        pygame.display.flip()

    def _draw_grid(self):
        """Draws the grid lines."""
        for x in range(self.grid_dims[0] + 1):
            start_pos = (self.grid_offset_x + x * self.cell_size, self.grid_offset_y)
            end_pos = (self.grid_offset_x + x * self.cell_size, self.grid_offset_y + self.grid_render_height)
            pygame.draw.line(self.screen, COLOR_GRID_LINES, start_pos, end_pos)

        for y in range(self.grid_dims[1] + 1):
            start_pos = (self.grid_offset_x, self.grid_offset_y + y * self.cell_size)
            end_pos = (self.grid_offset_x + self.grid_render_width, self.grid_offset_y + y * self.cell_size)
            pygame.draw.line(self.screen, COLOR_GRID_LINES, start_pos, end_pos)

    def _draw_obstacles(self, grid):
        """Draw the obstacles on the grid."""
        for obs in grid.get_obstacles():
            rect = pygame.Rect(
                self.grid_offset_x + obs[0] * self.cell_size,
                self.grid_offset_y + obs[1] * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            pygame.draw.rect(self.screen, COLOR_OBSTACLE, rect)

    def _draw_drones(self, drones):
        """Draws the drones and their IDs on the grid."""
        if not self.drone_image:
            self.logger.warning("Cannot draw drones, image not loaded.")
            return

        for drone in drones:
            # drone.position is a tuple (x, y), so we unpack it
            drone_x, drone_y = drone.position

            # Center the image within the cell
            center_x = self.grid_offset_x + drone_x * self.cell_size + self.cell_size / 2
            center_y = self.grid_offset_y + drone_y * self.cell_size + self.cell_size / 2
            
            # Get the rect for the image and center it
            img_rect = self.drone_image.get_rect(center=(center_x, center_y))
            self.screen.blit(self.drone_image, img_rect)
            
            # Create a text surface for the drone's ID
            id_text = f"ID: {drone.drone_id}"
            text_surface = self.font.render(id_text, True, COLOR_TEXT)
            
            # Position the text slightly above the drone image
            text_rect = text_surface.get_rect(center=(center_x, center_y - self.cell_size * 0.5))
            self.screen.blit(text_surface, text_rect)
