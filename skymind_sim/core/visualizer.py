# skymind_sim/core/visualizer.py

import pygame

# --- Constants for Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)

# --- Constants for Drawing ---
DRONE_COLOR = BLUE
DRONE_INACTIVE_COLOR = GRAY
PATH_COLOR = GREEN
TARGET_COLOR = RED


class Visualizer:
    """
    Handles the graphical representation of the simulation using Pygame.
    """
    def __init__(self, width, height):
        """
        Initializes the Pygame window and visualizer settings.

        Args:
            width (int): The width of the simulation window.
            height (int): The height of the simulation window.
        """
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("SkyMind Drone Simulation")
        # Use a default system font. If not found, Pygame has a fallback.
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, drones, environment):
        """
        Draws the current state of the simulation onto the screen.
        
        Args:
            drones (list): A list of Drone objects to draw.
            environment (Environment): The simulation environment (unused for now, but good practice).
        """
        # 1. Fill the background
        self.screen.fill(WHITE)

        # 2. Draw each drone and its associated info
        for drone in drones:
            drone_pos = (int(drone.position[0]), int(drone.position[1]))
            
            # Choose color based on active status
            current_drone_color = DRONE_COLOR if drone.is_active else DRONE_INACTIVE_COLOR
            
            # Draw drone body
            pygame.draw.circle(self.screen, current_drone_color, drone_pos, 8) # Drone is an 8px radius circle

            # Draw drone ID and battery status text
            info_text = f"{drone.id} | Bat: {drone.current_battery:.0f}"
            if not drone.is_active:
                info_text += " [INACTIVE]"
            
            text_surface = self.font.render(info_text, True, BLACK)
            self.screen.blit(text_surface, (drone_pos[0] + 12, drone_pos[1] - 10))

            # Draw the drone's remaining path
            if drone.is_active and not drone.is_mission_complete and len(drone.path) > 0:
                # The path starts from the drone's current position to its next target
                path_points = [drone.position] + drone.path[drone.path_index:]
                if len(path_points) > 1:
                    # Convert all points to tuples of integers for drawing
                    drawable_points = [tuple(map(int, p)) for p in path_points]
                    pygame.draw.lines(self.screen, PATH_COLOR, False, drawable_points, 1)
            
                # Draw the current target as a hollow circle
                target_pos = drone.path[drone.path_index]
                pygame.draw.circle(self.screen, TARGET_COLOR, tuple(map(int, target_pos)), 5, 1)

        # 3. Update the entire display
        pygame.display.flip()

    def close(self):
        """Closes the Pygame window."""
        pygame.quit()
