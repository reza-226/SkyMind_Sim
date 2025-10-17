# FILE: skymind_sim/layer_2_models/energy_model.py

import logging
from skymind_sim.utils.config_manager import ConfigManager

class EnergyModel:
    """
    Manages the energy consumption and capacity of an entity (e.g., a drone).
    It loads a specific energy model's parameters from the configuration.
    """
    def __init__(self, model_name: str, owner_id: str):
        """
        Initializes the energy model for a specific owner.

        Args:
            model_name (str): The name of the energy model to load from config.
            owner_id (str): The unique identifier of the entity that owns this model.
        """
        # Use owner_id for a more specific and useful logger
        self.logger = logging.getLogger(f"{self.__class__.__name__}.{owner_id}.{model_name}")
        self.config = ConfigManager()
        self.model_name = model_name
        self.owner_id = owner_id  # Store the owner's ID

        self.params = self._load_model_params()

        # Safely get capacity, raising an error if not found
        self.capacity = self.params.get('capacity_joules')
        if self.capacity is None:
            self.logger.critical(f"Missing 'capacity_joules' for energy model '{self.model_name}'")
            raise ValueError(f"Missing 'capacity_joules' for energy model '{self.model_name}'")

        # Set initial charge to capacity if not specified
        self.current_charge = self.params.get('initial_charge_joules', self.capacity)

        self.logger.info(
            f"Energy model '{self.model_name}' initialized for owner '{self.owner_id}' "
            f"with capacity {self.capacity}J and initial charge {self.current_charge}J."
        )

    def _load_model_params(self):
        """Loads parameters for the specified energy model from the config."""
        key = f"energy.models.{self.model_name}"
        params = self.config.get(key)
        if params is None or not isinstance(params, dict):
            self.logger.error(f"Energy model parameters not found or invalid for key: '{key}'")
            # Return an empty dict to prevent a crash, but subsequent operations will fail.
            return {}
        return params

    def get_charge_percentage(self) -> float:
        """Returns the current charge as a percentage of the total capacity."""
        if self.capacity == 0:
            return 0.0
        return (self.current_charge / self.capacity) * 100

    def consume(self, joules: float) -> bool:
        """
        Consumes a specific amount of energy. Returns True on success, False on failure.
        """
        if joules < 0:
            self.logger.warning("Attempted to consume a negative amount of energy. Ignoring.")
            return True  # Operation is not a failure

        if self.current_charge >= joules:
            self.current_charge -= joules
            self.logger.debug(f"Consumed {joules}J. New charge: {self.current_charge}J.")
            return True
        else:
            self.logger.warning(
                f"Not enough energy to consume {joules}J. "
                f"Required: {joules}J, Available: {self.current_charge}J."
            )
            # Option: Deplete the remaining charge completely
            # self.current_charge = 0
            return False
