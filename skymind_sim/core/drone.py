# skymind_sim/core/drone.py

import numpy as np

class Drone:
    """
    Represents a single drone in the simulation.
    """
    _id_counter = 0

    @classmethod
    def _generate_id(cls):
        cls._id_counter += 1
        return cls._id_counter

    def __init__(self, position: np.ndarray, velocity: np.ndarray = np.zeros(3)):
        """
        Initializes a Drone.

        Args:
            position (np.ndarray): The initial position [x, y, z] of the drone.
            velocity (np.ndarray, optional): The initial velocity [vx, vy, vz] of the drone. 
                                             Defaults to [0, 0, 0].
        """
        self.drone_id = self._generate_id()
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.target = None
        self.speed = 0.0

    def set_mission(self, target: np.ndarray, speed: float):
        """
        Assigns a simple "fly to target" mission to the drone.

        Args:
            target (np.ndarray): The destination coordinates [x, y, z].
            speed (float): The desired speed for the mission.
        """
        self.target = np.array(target, dtype=float)
        self.speed = float(speed)
        print(f"  - Drone {self.drone_id} assigned to fly to {self.target} with speed {self.speed}")

    def update_state(self, dt: float):
        """
        Updates the drone's position and velocity based on its mission and the time step.

        Args:
            dt (float): The time delta for this simulation step.
        """
        if self.target is None:
            # If there's no mission, the drone doesn't move.
            self.velocity = np.zeros(3)
            return

        # Vector from current position to target
        direction_vector = self.target - self.position
        distance_to_target = np.linalg.norm(direction_vector)

        # Check if the drone is already at or very close to the target
        if distance_to_target < 0.1:  # A small threshold to avoid jittering
            self.velocity = np.zeros(3)
            return

        # Normalize the direction vector to get a unit vector
        direction_unit_vector = direction_vector / distance_to_target

        # Set the velocity vector
        self.velocity = direction_unit_vector * self.speed

        # Update the position based on the new velocity and time step
        displacement = self.velocity * dt
        if np.linalg.norm(displacement) > distance_to_target:
            # If the next step would overshoot, just move directly to the target
            self.position = self.target
        else:
            self.position += displacement

    def __repr__(self):
        return (f"Drone(ID={self.drone_id}, Pos={self.position}, Vel={self.velocity}, "
                f"Target={self.target}, Speed={self.speed})")
