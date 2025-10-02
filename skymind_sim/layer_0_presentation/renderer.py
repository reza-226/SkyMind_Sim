# skymind_sim/layer_0_presentation/renderer.py

import pygame
import logging
from .asset_loader import AssetLoader

logger = logging.getLogger(__name__)

class Renderer:
    """
    Handles all rendering tasks for the simulation.
    It takes the world state from Layer 1 and draws it on the screen.
    This is the core of Layer 0.
    """
    # Define colors
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    COLOR_OBSTACLE = (100, 100, 100)
    COLOR_DRONE_PATH = (200, 200, 255)
    COLOR_DRONE_TARGET = (255, 0, 0)

    def __init__(self, width: int, height: int, title: str = "SkyMind_Sim"):
        """
        Initializes the renderer and the pygame window.

        Args:
            width (int): The width of the simulation window.
            height (int): The height of the simulation window.
            title (str): The title of the simulation window.
        """
        self.width = width
        self.height = height
        self.title = title
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        
        self.assets = {}
        self.font = None
        self.asset_loader = AssetLoader()
        
        logger.info(f"Renderer initialized with size ({width}x{height}) and title '{title}'.")

    def load_assets(self):
        """
        Loads all required assets like images and fonts, and processes them if needed.
        """
        try:
            # 1. Load the original image using the asset loader.
            original_drone_img = self.asset_loader.load_image('drone.png')
            # 2. Scale the image to the desired size for rendering.
            self.assets['drone'] = pygame.transform.scale(original_drone_img, (40, 40))

            self.font = self.asset_loader.load_font('Roboto-Regular.ttf', 16)
            logger.info("Assets loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load assets: {e}", exc_info=True)
            # As a fallback, we set the asset to None. The render methods will handle this.
            self.assets['drone'] = None

    def render(self, world_state: dict):
        """
        Renders a single frame of the simulation.

        Args:
            world_state (dict): A dictionary containing the current state of all entities.
        """
        # 1. Fill background
        self.screen.fill(self.COLOR_WHITE)

        # 2. Render obstacles
        for obstacle in world_state.get("obstacles", []):
            self._draw_obstacle(obstacle)

        # 3. Render drones and their paths
        for drone in world_state.get("drones", []):
            self._draw_drone_path(drone)
            self._draw_drone(drone)

        # 4. Update the display
        pygame.display.flip()

    def _draw_drone(self, drone_state: dict):
        """Helper to draw a single drone."""
        pos = drone_state['position']
        if self.assets.get('drone'):
            # Pygame rects use top-left, so we adjust for the image center
            img = self.assets['drone']
            img_rect = img.get_rect(center=pos)
            self.screen.blit(img, img_rect)
        else:
            # Fallback to a simple circle if image fails to load
            pygame.draw.circle(self.screen, self.COLOR_BLACK, (int(pos[0]), int(pos[1])), 15)

        # Draw drone ID
        if self.font:
            id_text = self.font.render(drone_state['id'], True, self.COLOR_BLACK)
            self.screen.blit(id_text, (pos[0] + 20, pos[1] - 20))

    def _draw_obstacle(self, obstacle_state: dict):
        """Helper to draw a single obstacle."""
        rect = pygame.Rect(
            obstacle_state['position'][0],
            obstacle_state['position'][1],
            obstacle_state['size'][0],
            obstacle_state['size'][1]
        )
        pygame.draw.rect(self.screen, self.COLOR_OBSTACLE, rect)
        
        if self.font:
            id_text = self.font.render(obstacle_state['id'], True, self.COLOR_WHITE)
            text_rect = id_text.get_rect(center=rect.center)
            self.screen.blit(id_text, text_rect)


    def _draw_drone_path(self, drone_state: dict):
        """Helper to draw the drone's current path."""
        path = drone_state.get('path', [])
        if len(path) > 1:
            pygame.draw.lines(self.screen, self.COLOR_DRONE_PATH, False, path, 2)
        
        # Draw the final target point
        if path:
            target_pos = path[-1]
            pygame.draw.circle(self.screen, self.COLOR_DRONE_TARGET, (int(target_pos[0]), int(target_pos[1])), 5)

    def cleanup(self):
        """Performs cleanup tasks before closing."""
        logger.info("Renderer cleanup.")
