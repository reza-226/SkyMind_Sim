# =========================================================================
#  File: skymind_sim/layer_1_simulation/scheduler.py
#  Author: Reza & AI Assistant | 2025-10-14 (Standardized Version)
#  Description: Manages the sequence of actions for all agents.
# =========================================================================

import logging

class Scheduler:
    """
    زمان‌بند، ترتیب اجرای عوامل (agents) را در شبیه‌سازی مدیریت می‌کند.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.agents = []
        self.logger.info("Scheduler initialized.")

    def add(self, agent):
        """یک عامل را به لیست زمان‌بندی اضافه می‌کند."""
        self.agents.append(agent)
        self.logger.info(f"Agent '{agent}' added to the scheduler.")

    def step(self):
        """
        یک گام شبیه‌سازی را برای تمام عوامل اجرا می‌کند.
        متد step() هر عامل را به ترتیب فراخوانی می‌کند.
        """
        self.logger.debug(f"Scheduler starting new step for {self.get_agent_count()} agents.")
        for agent in self.agents:
            agent.step()
        self.logger.debug("Scheduler step finished.")
        
    # --- START: THIS IS THE NEW METHOD TO ADD ---
    def get_agent_count(self) -> int:
        """
        تعداد عوامل فعال در زمان‌بند را برمی‌گرداند.

        Returns:
            int: تعداد عوامل.
        """
        return len(self.agents)
    # --- END: NEW METHOD ---
