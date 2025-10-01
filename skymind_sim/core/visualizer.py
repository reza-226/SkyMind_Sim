# skymind_sim/core/visualizer.py

import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

class Visualizer:
    """
    Handles all the drawing and rendering for the simulation.
    """
    def __init__(self, screen, width, height):
        """
        Initializes the visualizer.

        Args:
            screen: The pygame screen surface to draw on.
            width (int): The width of the screen.
            height (int): The height of the screen.
        """
        self.screen = screen
        self.width = width
        self.height = height
        
        # --- MODIFIED SECTION ---
        # Try to load the drone image, but handle errors gracefully.
        try:
            self.drone_image = pygame.image.load('data/assets/drone_icon.png').convert_alpha()
            self.drone_image = pygame.transform.scale(self.drone_image, (30, 30))
        except (pygame.error, FileNotFoundError):
            # If the image file is not found or fails to load, print a warning 
            # and set the image to None. The drawing code will then use a fallback.
            print("Warning: 'data/assets/drone_icon.png' not found. Drawing circles for drones instead.")
            self.drone_image = None
        # --- END OF MODIFIED SECTION ---
        
        # Font for displaying text
        self.font = pygame.font.SysFont('Arial', 14)

    def draw(self, environment):
        """
        Draws the entire simulation state.

        Args:
            environment (Environment): The environment object containing all elements to draw.
        """
        self.screen.fill(WHITE)
        
        for drone in environment.drones:
            self.draw_drone(drone)

        pygame.display.flip()

    def draw_drone(self, drone):
        """
        Draws a single drone and its associated information.

        Args:
            drone (Drone): The drone object to draw.
        """
        pos = (int(drone.position[0]), int(drone.position[1]))

        # Draw Drone Path/Waypoints
        if drone.mission_path:
            points = [drone.position] + drone.mission_path
            if len(points) > 1:
                pygame.draw.lines(self.screen, GRAY, False, points, 2)
            
            for point in drone.mission_path:
                pygame.draw.circle(self.screen, BLUE, (int(point[0]), int(point[1])), 4)

        # Draw Drone Body
        if self.drone_image:
            img_rect = self.drone_image.get_rect(center=pos)
            self.screen.blit(self.drone_image, img_rect)
        else:
            # Fallback to drawing a circle if no image
            pygame.draw.circle(self.screen, BLACK, pos, 10)

        # Draw Drone Info (ID and Battery)
        id_text = self.font.render(drone.drone_id, True, BLACK)
        self.screen.blit(id_text, (pos[0] + 15, pos[1] - 15))
        
        battery_percentage = drone.battery / 100.0
        battery_bar_width = 30
        battery_bar_height = 5
        
        bg_rect = pygame.Rect(pos[0] - 15, pos[1] + 15, battery_bar_width, battery_bar_height)
        pygame.draw.rect(self.screen, RED, bg_rect)
        
        fg_width = int(battery_bar_width * battery_percentage)
        fg_rect = pygame.Rect(pos[0] - 15, pos[1] + 15, fg_width, battery_bar_height)
        pygame.draw.rect(self.screen, GREEN, fg_rect)
