# skymind_sim/core/drone.py

import logging

logger = logging.getLogger("simulation_log")

class Drone:
    """
    Represents a single drone in the simulation.
    
    Manages its own state, including ID, position, and path.
    """
    def __init__(self, drone_id, start_pos, char='D'):
        self.id = drone_id
        self.position = start_pos  # Current position as a tuple (row, col)
        self.char = char           # Character to represent the drone on the map
        self.path = []             # List of coordinates (tuples) to follow
        self.finished = False      # Flag to indicate if the drone has reached its destination
        logger.info(f"Drone '{self.id}' created at position {self.position}.")

    def move(self):
        """
        Moves the drone one step along its path.
        
        If the path is not empty, it pops the next coordinate from the path
        and updates its current position. If the path becomes empty after moving,
        it marks itself as finished.
        """
        if self.path and not self.finished:
            # Get the next position from the path
            next_pos = self.path.pop(0)
            self.position = next_pos
            logger.debug(f"Drone '{self.id}' moved to {self.position}.")
            
            # If the path is now empty, the drone has reached its destination
            if not self.path:
                self.finished = True
                logger.info(f"Drone '{self.id}' has reached its destination at {self.position}.")
        elif self.finished:
            logger.debug(f"Drone '{self.id}' has already finished its path.")
        else:
            # This case happens if a drone was created but never given a path
            logger.warning(f"Drone '{self.id}' has no path to follow. It remains at {self.position}.")

    def has_finished(self):
        """
        Returns True if the drone has completed its path.
        """
        return self.finished

    def __repr__(self):
        return f"Drone(id={self.id}, pos={self.position})"
