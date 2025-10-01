# skymind_sim/core/battery.py

class Battery:
    """
    Manages the battery state of a drone.
    """
    def __init__(self, capacity: float, charge_rate: float, discharge_rate_idle: float, discharge_rate_flight: float):
        """
        Initializes the battery.

        Args:
            capacity (float): Total capacity of the battery (e.g., in percentage, 100.0).
            charge_rate (float): Rate at which the battery charges per second.
            discharge_rate_idle (float): Rate at which the battery discharges per second when idle.
            discharge_rate_flight (float): Rate at which the battery discharges per second during flight.
        """
        self.capacity = capacity
        self.level = capacity  # Start with a full battery
        self.charge_rate = charge_rate
        self.discharge_rate_idle = discharge_rate_idle
        self.discharge_rate_flight = discharge_rate_flight

    def discharge(self, duration: float, is_flying: bool = True):
        """
        Discharges the battery for a given duration.

        Args:
            duration (float): The time duration in seconds.
            is_flying (bool): True if the drone is flying, False if idle.
        """
        if is_flying:
            discharge_amount = self.discharge_rate_flight * duration
        else:
            discharge_amount = self.discharge_rate_idle * duration
        
        self.level = max(0, self.level - discharge_amount)

    def charge(self, duration: float):
        """
        Charges the battery for a given duration.

        Args:
            duration (float): The time duration in seconds.
        """
        charge_amount = self.charge_rate * duration
        self.level = min(self.capacity, self.level + charge_amount)

    def get_level_percentage(self) -> float:
        """
        Returns the current battery level as a percentage.
        """
        return (self.level / self.capacity) * 100
