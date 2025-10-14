# =========================================================================
#  File: skymind_sim/layer_1_simulation/scheduler.py
#  Author: Reza & AI Assistant | 2025-10-14 (Refactored Version)
# =========================================================================
import logging
from typing import List

class Scheduler:
    """
    مدیریت ترتیب و زمان‌بندی اجرای عوامل (agents) در شبیه‌سازی.
    """
    def __init__(self):
        """سازنده زمان‌بند."""
        self.agents: List[object] = []
        self.logger = logging.getLogger(__name__)
        self.logger.info("Scheduler initialized.")

    def add(self, agent: object):
        """
        یک عامل جدید را به لیست زمان‌بندی اضافه می‌کند.
        عامل باید متد step() داشته باشد.
        """
        if not hasattr(agent, 'step'):
            self.logger.error(f"Attempted to add an agent of type {type(agent).__name__} which has no 'step' method.")
            raise AttributeError("Agent must have a 'step' method to be added to the scheduler.")
            
        self.agents.append(agent)
        self.logger.info(f"Agent '{agent}' added to the scheduler.")

    def remove(self, agent: object):
        """یک عامل را از زمان‌بند حذف می‌کند."""
        try:
            self.agents.remove(agent)
            self.logger.info(f"Agent '{agent}' removed from the scheduler.")
        except ValueError:
            self.logger.warning(f"Attempted to remove agent '{agent}' which was not in the scheduler.")

    def step(self):
        """
        متد step() را برای تمام عوامل ثبت‌شده به ترتیب فراخوانی می‌کند.
        این متد قلب تپنده شبیه‌ساز است.
        """
        self.logger.debug(f"Scheduler starting step for {len(self.agents)} agents.")
        
        # در آینده می‌توان ترتیب اجرای عوامل را تصادفی کرد تا منصفانه‌تر باشد.
        # import random
        # random.shuffle(self.agents)
        
        for agent in self.agents:
            try:
                agent.step()
            except Exception as e:
                self.logger.error(f"Error executing step for agent {agent}: {e}", exc_info=True)
        
        self.logger.debug("Scheduler finished step.")

    def get_agent_count(self) -> int:
        """تعداد عوامل فعال در زمان‌بند را برمی‌گرداند."""
        return len(self.agents)
