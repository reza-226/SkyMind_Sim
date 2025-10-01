# skymind_sim/core/battery.py

class Battery:
    """
    Represents the battery of a drone.
    """
    def __init__(self, initial_level: float = 100.0, min_level: float = 0.0, max_level: float = 100.0):
        """
        Initializes the battery.

        Args:
            initial_level (float): The starting battery level, as a percentage.
            min_level (float): The minimum battery level (usually 0).
            max_level (float): The maximum battery level (usually 100).
        """
        self.max_level = max_level
        self.min_level = min_level
        self.level = self._clamp(initial_level)

    def _clamp(self, value: float) -> float:
        """Ensures the battery level stays within the min/max bounds."""
        return max(self.min_level, min(self.max_level, value))

    def deplete(self, amount: float):
        """
        Depletes the battery by a given amount.

        Args:
            amount (float): The amount to deplete. Should be a positive number.
        """
        if amount > 0:
            self.level = self._clamp(self.level - amount)

    def charge(self, amount: float):
        """
        Charges the battery by a given amount.

        Args:
            amount (float): The amount to charge. Should be a positive number.
        """
        if amount > 0:
            self.level = self._clamp(self.level + amount)

    def is_empty(self) -> bool:
        """Checks if the battery is at its minimum level."""
        return self.level <= self.min_level

    def __repr__(self) -> str:
        """String representation of the battery status."""
        return f"<Battery: {self.level:.2f}%>"
