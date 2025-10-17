# skymind_sim/layer_0_presentation/input_handler.py

import pygame
from pygame.math import Vector2

class InputHandler:
    """Handles user input, converting keyboard and window events into game actions."""

    def __init__(self):
        pass

    def handle_events(self):
        """
        Process the Pygame event queue.
        
        Returns:
            dict: A dictionary containing actions like 'quit' (bool) and 
                  'movement_intent' (Vector2).
        """
        movement_intent = Vector2(0, 0)
        quit_event = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_event = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit_event = True

        # Handle continuous key presses for smooth movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            movement_intent.y = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            movement_intent.y = 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            movement_intent.x = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            movement_intent.x = 1
            
        # Normalize the vector to prevent faster diagonal movement
        if movement_intent.length() > 0:
            movement_intent = movement_intent.normalize()

        return {
            "quit": quit_event,
            "movement_intent": movement_intent
        }
