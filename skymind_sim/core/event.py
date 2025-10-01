# skymind_sim/core/event.py

from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Optional

class EventType(Enum):
    """Defines the types of events that can occur in the simulation."""
    DRONE_UPDATE = "DRONE_UPDATE"
    # Future event types can be added here, e.g., MISSION_COMMAND

@dataclass(order=True)
class Event:
    """Represents an event in the simulation priority queue."""
    # The 'time' of the event. Used for sorting in the priority queue.
    time: float = field(init=True, repr=True)
    
    # The 'type' of the event.
    type: EventType = field(init=True, repr=True)
    
    # The ID of the drone this event pertains to.
    drone_id: Optional[str] = field(default=None, compare=False, repr=True)
    
    # Optional payload for the event
    data: Optional[Any] = field(default=None, compare=False, repr=False)
