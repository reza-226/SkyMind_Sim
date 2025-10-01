# skymind_sim/core/simulation.py

import time
import pygame

class Simulation:
    """
    Manages the main simulation loop, state updates, and rendering.
    It orchestrates the interaction between the environment, drones, and visualizer.
    """
    def __init__(self, environment, visualizer, end_time):
        """
        Initializes the simulation manager.

        Args:
            environment (Environment): The simulation environment object.
            visualizer (Visualizer): The visualizer object for rendering.
            end_time (float): The total duration of the simulation in seconds.
        """
        self.environment = environment
        self.visualizer = visualizer
        self.end_time = end_time
        
        self.drones = []
        self.is_running = False
        self.current_time = 0.0
        self.clock = pygame.time.Clock()

    def add_drone(self, drone):
        """Adds a drone to the simulation."""
        self.drones.append(drone)
        print(f"Added drone to simulation: {drone.id}")

    def run(self):
        """
        Starts and executes the main simulation loop.
        The loop continues until the end time is reached or the window is closed.
        """
        self.is_running = True
        
        while self.is_running:
            # 1. Handle Events (like closing the window)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
            
            # 2. Calculate time delta (dt)
            # This makes the simulation speed independent of the computer's speed.
            # We cap the frame rate at 60 FPS. dt will be in seconds.
            dt = self.clock.tick(60) / 1000.0

            # 3. Update simulation state
            self.current_time += dt
            if self.current_time >= self.end_time:
                print("Simulation end time reached.")
                self.is_running = False

            # Update each drone
            for drone in self.drones:
                drone.update(dt)

            # 4. Render the new state
            # We pass the list of drones and the environment to the visualizer
            self.visualizer.draw(self.drones, self.environment)
            
        print("Simulation loop has ended.")

    def close(self):
        """A helper method to cleanly close the visualizer."""
        if self.visualizer:
            self.visualizer.close()
