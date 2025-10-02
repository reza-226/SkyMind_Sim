import logging

logger = logging.getLogger(__name__)

class World:
    """
    Represents the simulation environment, including its dimensions and entities.
    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.drones = []
        self.obstacles = []
        logger.info(f"World created with size ({self.width}x{self.height}).")

    def add_drone(self, drone):
        self.drones.append(drone)
        logger.info(f"Added {drone} to the world.")

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)
        logger.info(f"Added {obstacle} to the world.")
