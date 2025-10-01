# skymind_sim/core/environment.py

from typing import Tuple

class Environment:
    """
    Represents the physical environment of the simulation.
    
    This class holds properties of the simulation world, such as its
    dimensions. In the future, it could also manage obstacles, weather
    conditions, or other environmental factors.
    """
    def __init__(self, size: Tuple[int, int]):
        """
        Initializes the environment.

        Args:
            size (Tuple[int, int]): The dimensions of the environment as (width, height).
        """
        if not (isinstance(size, (tuple, list)) and len(size) == 2 and
                all(isinstance(x, (int, float)) for x in size)):
            raise ValueError("size must be a tuple or list of two numbers (width, height).")
            
        self.size = size
        self.width, self.height = self.size

    def __repr__(self) -> str:
        """
        Provides a string representation of the Environment object.
        """
        return f"Environment(size=({self.width}, {self.height}))"
