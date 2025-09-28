# tests/test_simulation.py
# ... (کدهای import و بقیه تست‌ها را دست نزنید)

import pytest
import numpy as np
from skymind_sim.core.environment import Environment
from skymind_sim.core.drone import Drone, DroneStatus
from skymind_sim.core.simulation import Simulation

# ... (سایر fixtureها و تست‌های این فایل)

@pytest.fixture
def basic_simulation():
    """
    Sets up a basic simulation with one drone in an environment.
    The drone is configured to be in a state ready for movement.
    """
    env = Environment(width=100, height=100, depth=100)
    drone = Drone(drone_id=1)
    
    # Configure the drone for movement
    initial_pos = np.array([10.0, 10.0, 10.0])
    initial_vel = np.array([1.0, 0.0, 0.0]) # Give it a non-zero velocity
    drone.move_to(initial_pos)
    drone.set_velocity(initial_vel)
    drone.status = DroneStatus.FLYING # Set status to FLYING!

    env.add_drone(drone)
    
    sim = Simulation(environment=env)
    return sim, drone, env

# ... (سایر تست‌ها)

def test_drone_moves_during_simulation(basic_simulation):
    """Test that the drone's position is updated after running the simulation."""
    sim, drone, _ = basic_simulation
    initial_position = drone.position.copy()

    # Sanity check: Ensure velocity is not zero
    assert not np.array_equal(drone.velocity, np.array([0.0, 0.0, 0.0]))
    
    num_steps = 5
    dt = 0.2
    sim.run(num_steps=num_steps, dt=dt)

    final_position = drone.position
    
    # Check that the position has actually changed
    assert not np.array_equal(initial_position, final_position), "Drone did not move!"
    
    # Check if the final position is correct based on physics
    # Total time = num_steps * dt = 5 * 0.2 = 1.0 seconds
    # Expected change = velocity * total_time = [1, 0, 0] * 1.0 = [1, 0, 0]
    expected_position = initial_position + drone.velocity * (num_steps * dt)
    assert np.allclose(final_position, expected_position), "Drone did not move to the correct final position."

# ... (سایر تست‌ها)
