# مسیر: skymind_sim/layer_0_presentation/pygame_renderer.py

import pygame
from typing import Optional, Any, Dict, List, Tuple

class PygameRenderer:
    """
    Handles all Pygame-related rendering, including the window, grid, and objects.
    """
    
    # ثابت‌ها برای خوانایی بهتر
    COLOR_BACKGROUND = (50, 50, 50)       # Dark Grey
    COLOR_GRID_LINES = (80, 80, 80)     # Lighter Grey
    COLOR_OBSTACLE = (200, 50, 50)        # Red
    CELL_SIZE = 25                        # Size of each grid cell in pixels

    def __init__(self, grid_width: int, grid_height: int, logger: Optional[Any] = None):
        """
        Initializes the Pygame window.
        The screen size is calculated based on grid dimensions and CELL_SIZE.
        """
        self.logger = logger
        self.grid_width = grid_width
        self.grid_height = grid_height
        
        # محاسبه ابعاد صفحه
        screen_width = self.grid_width * self.CELL_SIZE
        screen_height = self.grid_height * self.CELL_SIZE
        
        pygame.init()
        pygame.display.set_caption("SkyMind Drone Simulation")
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        
        self.log(f"Pygame screen initialized. Size: {screen_width}x{screen_height}", "info")

    def log(self, message: str, level: str = "info"):
        if self.logger:
            getattr(self.logger, level, self.logger.info)(message)
        else:
            print(f"RENDERER_{level.upper()}: {message}")

    def render(self, world_state: Dict[str, Any]):
        """Renders the entire simulation state based on the provided dictionary."""
        self.screen.fill(self.COLOR_BACKGROUND)
        self._draw_grid()
        
        # دریافت لیست موانع از world_state و رسم آنها
        obstacles = world_state.get("obstacles", [])
        self._draw_obstacles(obstacles)
        
        pygame.display.flip()

    def _draw_grid(self):
        """Draws the grid lines on the screen."""
        width, height = self.screen.get_size()
        for x in range(0, width, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.COLOR_GRID_LINES, (x, 0), (x, height))
        for y in range(0, height, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.COLOR_GRID_LINES, (0, y), (width, y))

    def _draw_obstacles(self, obstacles: List[Tuple[int, int]]):
        """Draws obstacles on the grid."""
        for ox, oy in obstacles:
            rect = pygame.Rect(
                ox * self.CELL_SIZE, 
                oy * self.CELL_SIZE, 
                self.CELL_SIZE, 
                self.CELL_SIZE
            )
            pygame.draw.rect(self.screen, self.COLOR_OBSTACLE, rect)

    def close(self):
        """Closes the Pygame window properly."""
        pygame.quit()
