# tests/test_drone.py

import pytest
from skymind_sim.core.drone import Drone

def test_drone_creation():
    """
    Tests if a drone is created with the correct initial attributes.
    """
    drone = Drone(drone_id=1, initial_position=(10, 20, 5))
    assert drone.id == 1
    assert drone.position == (10, 20, 5)
    assert drone.velocity == (0, 0, 0)
    assert drone.status == 'IDLE'
    print("\n✅ test_drone_creation: Passed")

def test_drone_representation():
    """
    Tests the __repr__ method for a clean output.
    """
    drone = Drone(drone_id=99)
    expected_repr = "Drone(id=99, position=(0, 0, 0), status='IDLE')"
    assert repr(drone) == expected_repr
    print("✅ test_drone_representation: Passed")

def test_drone_move():
    """
    Tests the move method and status update.
    """
    drone = Drone(drone_id=2)
    drone.move(new_position=(50, 50, 50))
    assert drone.position == (50, 50, 50)
    assert drone.status == 'FLYING'
    print("✅ test_drone_move: Passed")

def test_drone_land():
    """
    Tests the land method and status update.
    """
    drone = Drone(drone_id=3, initial_position=(1, 1, 1))
    # First, it must be flying to be able to land
    drone.update_status('FLYING')
    
    drone.land()
    assert drone.status == 'IDLE'
    print("✅ test_drone_land: Passed")

def test_invalid_drone_id():
    """
    Tests that creating a drone with an invalid ID raises a TypeError.
    """
    with pytest.raises(TypeError):
        Drone(drone_id="not-an-int")
    print("✅ test_invalid_drone_id: Passed")

def test_invalid_position():
    """
    Tests that creating a drone with an invalid position raises a ValueError.
    """
    with pytest.raises(ValueError):
        Drone(drone_id=4, initial_position=(10, 20)) # Missing z-coordinate
    print("✅ test_invalid_position: Passed")
