# skymind_sim/core/environment.py
import pygame

class Environment:
    def __init__(self, config):
        """
        Initializes the simulation environment, including Pygame and the display window.
        """
        print("INFO: Initializing Environment...")
        self.config = config
        
        # --- CRITICAL INITIALIZATION STEPS ---
        # 1. Initialize all imported Pygame modules
        pygame.init()
        print("INFO: Pygame initialized successfully.")

        # 2. Get screen dimensions from config
        screen_width = self.config.get('SCREEN_WIDTH', 1280)
        screen_height = self.config.get('SCREEN_HEIGHT', 720)
        
        # 3. Create the display surface (the main window)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        print(f"INFO: Display set to {screen_width}x{screen_height}.")
        
        pygame.display.set_caption(self.config.get('CAPTION', 'SkyMind Drone Simulator'))
        
        self.clock = pygame.time.Clock()
        self.running = True

        print("INFO: Environment created.")

    def update(self):
        """
        Placeholder for updating environment state (e.g., moving obstacles).
        """
        pass

    def render(self, *sprite_groups):
        """
        Renders all visual elements to the screen.
        """
        # Fill the background
        self.screen.fill(self.config.get('BACKGROUND_COLOR', (20, 30, 40)))

        # Draw all sprites from the provided groups
        for group in sprite_groups:
            group.draw(self.screen)

        # Update the full display Surface to the screen
        pygame.display.flip()

    def handle_events(self, events):
        """
        Handles global events like quitting the application.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
