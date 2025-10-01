# skymind_sim/core/environment.py

class Environment:
    """
    Represents the simulation environment, including its dimensions.
    For now, it just holds the boundaries of the world.
    In the future, it can be extended to include obstacles, weather, etc.
    """
    def __init__(self, width, height):
        """
        Initializes the environment.

        Args:
            width (int or float): The width of the simulation area.
            height (int or float): The height of the simulation area.
        """
        self.width = int(width)
        self.height = int(height)

    def __repr__(self):
        """Provides a developer-friendly representation of the environment."""
        return f"Environment(width={self.width}, height={self.height})"
