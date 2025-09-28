# tests/test_environment.py

import pytest
import numpy as np
from skymind_sim.core.environment import Environment
from skymind_sim.core.drone import Drone

@pytest.fixture
def empty_environment():
    """Provides a clean environment for each test."""
    return Environment(width=200, height=200, depth=100)

def test_environment_initialization(empty_environment):
    """Tests if the environment is initialized correctly."""
    assert empty_environment.width == 200
    assert empty_environment.height == 200
    assert empty_environment.depth == 100
    assert empty_environment.drones == {}  # Should be an empty dictionary
    assert empty_environment.drones_count == 0

def test_environment_invalid_dimensions():
    """Tests that initializing with non-positive dimensions raises an error."""
    with pytest.raises(ValueError, match="must be positive"):
        Environment(width=-100, height=100)
    with pytest.raises(ValueError, match="must be positive"):
        Environment(width=100, height=0)

def test_add_drone_to_environment(empty_environment):
    """Tests adding a valid drone to the environment."""
    drone = Drone(drone_id=1)
    drone.position = np.array([50.0, 50.0, 50.0]) # Set position after creation
    empty_environment.add_drone(drone)
    
    assert empty_environment.drones_count == 1
    assert empty_environment.get_drone(1) == drone
    assert 1 in empty_environment.drones

def test_add_duplicate_drone_raises_error(empty_environment):
    """Tests that adding a drone with a duplicate ID raises a ValueError."""
    drone1 = Drone(drone_id=1)
    drone1.position = np.array([10.0, 10.0, 10.0])
    empty_environment.add_drone(drone1)
    
    drone2_duplicate = Drone(drone_id=1) # Same ID
    drone2_duplicate.position = np.array([20.0, 20.0, 20.0])

    with pytest.raises(ValueError, match="already exists"):
        empty_environment.add_drone(drone2_duplicate)

def test_add_drone_outside_boundaries_raises_error(empty_environment):
    """Tests that adding a drone outside the environment boundaries raises an error."""
    drone_outside = Drone(drone_id=2)
    drone_outside.position = np.array([300.0, 50.0, 50.0]) # x is out of bounds (width=200)
    
    with pytest.raises(ValueError, match="outside the environment boundaries"):
        empty_environment.add_drone(drone_outside)

def test_environment_representation(empty_environment):
    """Tests the __repr__ method of the Environment class."""
    drone = Drone(drone_id=1)
    drone.position = np.array([10.0, 20.0, 0.0])
    empty_environment.add_drone(drone)
    
    expected_repr = "Environment(width=200, height=200, depth=100, drones_count=1)"
    assert repr(empty_environment) == expected_repr
