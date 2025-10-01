# skymind_sim/core/visualizer.py

import pygame
from typing import Dict, Tuple
from .drone import Drone

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Visualizer:
    # The __init__ signature is the key part here. It explicitly defines 'size' and 'drones'.
    def __init__(self, size: Tuple[int, int], drones: Dict[str, Drone]):
        """
        Initializes the Pygame visualizer.

        Args:
            size (Tuple[int, int]): The dimensions of the simulation window (width, height).
            drones (Dict[str, Drone]): A dictionary of drone objects to be visualized.
        """
        pygame.init()
        pygame.display.set_caption("SkyMind Simulation")

        self.width, self.height = size
        self.screen = pygame.display.set_mode(size)
        self.drones = drones  # Store the dictionary of drones
        self.font = pygame.font.SysFont(None, 24)

    def _draw_drone(self, drone: Drone):
        """Draws a single drone and its path."""
        # Draw waypoints
        for i, wp in enumerate(drone.waypoints):
            color = GREEN if i >= drone.current_waypoint_index else BLUE
            pygame.draw.circle(self.screen, color, (int(wp[0]), int(wp[1])), 5)
            if i > 0:
                pygame.draw.line(self.screen, color, drone.waypoints[i-1], drone.waypoints[i], 1)

        # Draw the drone itself
        drone_pos = (int(drone.pos[0]), int(drone.pos[1]))
        pygame.draw.circle(self.screen, RED, drone_pos, 8) # Main body
        pygame.draw.circle(self.screen, WHITE, drone_pos, 8, 1) # Outline

        # Draw drone ID label
        id_text = self.font.render(drone.id, True, WHITE)
        self.screen.blit(id_text, (drone_pos[0] + 10, drone_pos[1]))

    def update(self) -> bool:
        """
        Updates the display with the current state of all drones.
        Returns False if the user has quit the application, True otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # Drawing
        self.screen.fill(BLACK)

        for drone_id, drone in self.drones.items():
            self._draw_drone(drone)

        pygame.display.flip()
        return True

    def close(self):
        """Closes the pygame window."""
        pygame.quit()
