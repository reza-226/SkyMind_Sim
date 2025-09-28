# tests/test_environment.py (نسخه نهایی اصلاح شده)

import pytest
from skymind_sim.core.environment import Environment
from skymind_sim.core.drone import Drone

def test_environment_initialization():
    """Tests if the environment is initialized correctly."""
    env = Environment(width=100.0, height=150.0)
    assert env.width == 100.0
    assert env.height == 150.0
    assert env.drones == []

def test_environment_invalid_dimensions():
    """Tests that initializing with non-positive dimensions raises an error."""
    with pytest.raises(ValueError):
        Environment(width=0, height=100)
    with pytest.raises(ValueError):
        Environment(width=100, height=-50)

def test_add_drone_to_environment():
    """Tests adding a valid drone to the environment."""
    env = Environment(width=100, height=100)
    drone = Drone(drone_id=1, initial_position=(50, 50, 0))
    env.add_drone(drone)
    assert len(env.drones) == 1
    assert env.drones[0] == drone
    # *** تغییر در این خط ***
    assert env.drones[0].id == 1

def test_add_drone_outside_boundaries():
    """Tests that adding a drone outside the environment boundaries raises an error."""
    env = Environment(width=100, height=100)
    drone_outside = Drone(drone_id=2, initial_position=(100, 50, 0))
    
    with pytest.raises(ValueError, match="outside the environment boundaries"):
        env.add_drone(drone_outside)
    
    assert len(env.drones) == 0

def test_environment_representation():
    """Tests the __repr__ method of the Environment class."""
    env = Environment(width=200, height=300)
    drone1 = Drone(drone_id=1, initial_position=(10, 20, 0))
    drone2 = Drone(drone_id=2, initial_position=(30, 40, 0))
    env.add_drone(drone1)
    env.add_drone(drone2)
    
    expected_repr = "Environment(width=200, height=300, drones_count=2)"
    assert repr(env) == expected_repr
