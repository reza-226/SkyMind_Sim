# tests/test_drone.py

import pytest
import numpy as np
from skymind_sim.core.drone import Drone, DroneStatus

def test_drone_creation():
    """Tests if a drone is created with the correct initial attributes."""
    drone = Drone(drone_id=1)
    
    assert drone.id == 1
    assert isinstance(drone.id, int)
    assert np.array_equal(drone.position, np.array([0.0, 0.0, 0.0]))
    assert np.array_equal(drone.velocity, np.array([0.0, 0.0, 0.0]))
    assert drone.status == DroneStatus.IDLE

def test_drone_creation_with_wrong_id_type():
    """Tests that creating a drone with a non-integer ID raises a TypeError."""
    with pytest.raises(TypeError, match="Drone ID must be an integer"):
        Drone(drone_id="d1")

def test_drone_representation():
    """Tests the __repr__ method for a clean output."""
    drone = Drone(drone_id=99)
    # The __repr__ in the new Drone class is: f"Drone(id={self.id}, status={self.status.name}, position={pos})"
    # Example: Drone(id=99, status=IDLE, position=[0.00, 0.00, 0.00])
    expected_repr = "Drone(id=99, status=IDLE, position=[0.00, 0.00, 0.00])"
    assert repr(drone) == expected_repr

def test_drone_move_to():
    """Tests the move_to method."""
    drone = Drone(drone_id=2)
    new_pos = np.array([50.0, 50.0, 50.0])
    drone.move_to(new_pos)
    assert np.array_equal(drone.position, new_pos)

def test_set_velocity():
    """Tests the set_velocity method."""
    drone = Drone(drone_id=3)
    new_vel = np.array([5.0, -5.0, 2.0])
    drone.set_velocity(new_vel)
    assert np.array_equal(drone.velocity, new_vel)

def test_invalid_position_in_move_to():
    """Tests that move_to with an invalid position raises a ValueError."""
    drone = Drone(drone_id=4)
    with pytest.raises(ValueError, match="Position must be a 3D numpy array."):
        drone.move_to(np.array([10, 20])) # Missing z-coordinate

def test_invalid_velocity_in_set_velocity():
    """Tests that set_velocity with an invalid vector raises a ValueError."""
    drone = Drone(drone_id=5)
    with pytest.raises(ValueError, match="Velocity must be a 3D numpy array."):
        drone.set_velocity(np.array([1, 2, 3, 4])) # Extra coordinate
