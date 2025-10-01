# FILE: skymind_sim/core/simulation.py

import pygame
from .visualizer import Visualizer

class Simulation:
    """
    The main simulation class that orchestrates the entire process.
    """
    def __init__(self, environment, screen, width, height):
        """
        Initializes the simulation.

        Args:
            environment (Environment): The simulation environment containing drones.
            screen (pygame.Surface): The Pygame screen surface for drawing.
            width (int): The width of the screen.
            height (int): The height of the screen.
        """
        self.environment = environment
        self.visualizer = Visualizer(screen, width, height)
        self.running = False
        self.clock = pygame.time.Clock()
        self.fps = 60

    def run(self):
        """
        Starts and runs the main simulation loop.
        """
        self.running = True
        while self.running:
            # --- Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Add other event handlers here (e.g., keyboard input)

            # --- Time Management ---
            # Get the time elapsed since the last frame in seconds
            delta_time = self.clock.tick(self.fps) / 1000.0

            # --- Simulation Logic Update ---
            self.environment.update_state(delta_time)

            # --- Rendering ---
            self.visualizer.draw(self.environment)

        print("Simulation finished.")
