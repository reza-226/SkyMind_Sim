# skymind_sim/core/event.py

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any

class EventType(Enum):
    """
    Defines the types of events that can occur in the simulation.
    """
    UPDATE_STATE = auto()  # Event to update a drone's state
    VISUALIZER_UPDATE = auto() # Event to update the visualization

@dataclass(order=True)
class Event:
    """
    Represents an event in the simulation priority queue.
    
    The 'order=True' argument makes Event objects comparable based on their fields,
    starting with 'timestamp'. This is crucial for the priority queue.
    """
    timestamp: float
    event_type: EventType = field(compare=False)
    data: Any = field(default=None, compare=False)
