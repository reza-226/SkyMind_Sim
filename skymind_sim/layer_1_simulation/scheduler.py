# skymind_sim/layer_1_simulation/scheduler.py

import logging

class Scheduler:
    """
    زمانبندی برای مدیریت و فعال‌سازی عامل‌ها (agents) در هر گام شبیه‌سازی.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._agents = []

    def add_agent(self, agent):
        """یک عامل جدید را به زمانبند اضافه می‌کند."""
        if agent not in self._agents:
            self._agents.append(agent)
            self.logger.info(f"Agent '{getattr(agent, 'id', 'unknown')}' added to scheduler.")
        else:
            self.logger.warning(f"Agent '{getattr(agent, 'id', 'unknown')}' is already in the scheduler.")

    def remove_agent(self, agent):
        """یک عامل را از زمانبند حذف می‌کند."""
        try:
            self._agents.remove(agent)
            self.logger.info(f"Agent '{getattr(agent, 'id', 'unknown')}' removed from scheduler.")
        except ValueError:
            self.logger.warning(f"Attempted to remove agent '{getattr(agent, 'id', 'unknown')}' which is not in the scheduler.")

    def step(self):
        """
        متد step() را برای تمام عامل‌های ثبت‌شده به ترتیب فراخوانی می‌کند.
        """
        if not self._agents:
            self.logger.debug("Scheduler step called, but no agents to process.")
            return
            
        for agent in self._agents:
            try:
                agent.step()
            except Exception as e:
                self.logger.error(f"Error during step for agent '{getattr(agent, 'id', 'unknown')}': {e}", exc_info=True)

    @property
    def agents(self):
        """یک ویژگی عمومی برای دسترسی فقط-خواندنی به لیست عامل‌ها."""
        return self._agents
