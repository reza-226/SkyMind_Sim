"""
This __init__.py file makes it easier to import core simulation components 
from the skymind_sim.core package.

By importing the main classes here, you can access them directly, like so:
from skymind_sim.core import Drone, Environment, Simulation

Instead of the longer path:
from skymind_sim.core.drone import Drone
from skymind_sim.core.environment import Environment
from skymind_sim.core.simulation import Simulation

This simplifies the import statements in other parts of the application,
such as in the main executable script or in notebooks.
"""

from .drone import Drone
from .environment import Environment  # FIX: Removed 'Obstacle' as it is not defined yet
from .simulation import Simulation
