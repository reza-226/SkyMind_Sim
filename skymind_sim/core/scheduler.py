# skymind_sim/core/scheduler.py

import heapq
from .event import Event

class Scheduler:
    def __init__(self):
        """Initializes an empty event queue."""
        self.event_queue = []

    def add_event(self, event: Event):
        """Adds an event to the priority queue."""
        heapq.heappush(self.event_queue, event)

    def get_next_event(self) -> Event | None:
        """Retrieves and removes the next event from the queue."""
        if not self.is_empty():
            return heapq.heappop(self.event_queue)
        return None

    def is_empty(self) -> bool:
        """Checks if the event queue is empty."""
        return not self.event_queue
