# path: skymind_sim/layer_1_simulation/scheduler.py

from typing import List, TYPE_CHECKING
from skymind_sim.utils.config_manager import ConfigManager
from skymind_sim.utils.log_manager import LogManager

if TYPE_CHECKING:
    from .entities.drone import Drone

class Scheduler:
    """Manages the order and timing of agent actions."""
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.logger = LogManager.get_logger(__name__)
        self.current_tick = 0
        self.agents: List['Drone'] = []
        self.logger.info("Scheduler initialized.")

    def add(self, agent: 'Drone'):
        """Adds an agent to the scheduler's list to be managed."""
        if agent not in self.agents:
            self.agents.append(agent)
            self.logger.info(f"Agent '{agent.get_id()}' added to the scheduler.")
        else:
            self.logger.warning(f"Attempted to add agent '{agent.get_id()}' which is already in the scheduler.")

    # -- START OF MODIFIED SECTION --
    def execute_tick(self):
        """Executes a single time step (tick) for all registered agents."""
        self.logger.debug(f"Executing tick {self.current_tick} for {len(self.agents)} agents.")
        
        if not self.agents:
            self.logger.debug("No agents in scheduler to execute.")
            self.current_tick += 1
            return

        for agent in self.agents:
            try:
                # Pass the current tick to the agent's step method
                agent.step(self.current_tick)
            except Exception as e:
                self.logger.error(f"Error during agent '{agent.get_id()}' step on tick {self.current_tick}: {e}", exc_info=True)
        
        self.current_tick += 1
    # -- END OF MODIFIED SECTION --
