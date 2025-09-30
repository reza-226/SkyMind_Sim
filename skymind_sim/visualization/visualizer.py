# skymind_sim/visualization/visualizer.py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class Visualizer3D:
    """
    Handles the 3D visualization of the simulation environment, obstacles, and path.
    """
    # --- تغییر ۱: افزودن start_point و end_point به __init__ ---
    def __init__(self, environment, start_point, end_point):
        """
        Initializes the 3D visualizer.

        Args:
            environment (Environment): The simulation environment.
            start_point (tuple): The (x, y, z) starting coordinate.
            end_point (tuple): The (x, y, z) ending coordinate.
        """
        self.env = environment
        # --- تغییر ۲: ذخیره کردن نقاط شروع و پایان ---
        self.start_point = start_point
        self.end_point = end_point
        
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        width, depth, height = self.env.get_dimensions()
        self.ax.set_xlim([0, width])
        self.ax.set_ylim([0, depth])
        self.ax.set_zlim([0, height])
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')
        self.ax.set_title('SkyMind 3D Simulation')

    def draw_obstacles(self):
        """Draws all obstacles in the environment as gray cubes."""
        obstacles = self.env.get_obstacles()
        if not obstacles:
            return

        # Prepare cube vertices
        cube_vertices = np.array([
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
        ])

        # Plot each obstacle
        for obs in obstacles:
            x, y, z = obs
            # Create a cube at the obstacle's position
            self.ax.bar3d(x, y, z, 1, 1, 1, color='gray', alpha=0.6, shade=True)

    def draw_path(self, path):
        """
        Draws the found path, including start and end points.
        """
        if not path:
            return

        # Unzip the path coordinates
        x_coords = [p[0] for p in path]
        y_coords = [p[1] for p in path]
        z_coords = [p[2] for p in path]
        
        # Draw the path line
        self.ax.plot(x_coords, y_coords, z_coords, color='blue', marker='o', linestyle='-', markersize=2, label='Path')

        # --- تغییر ۳: استفاده از نقاط ذخیره شده برای رسم ---
        # Draw start point (Green)
        self.ax.scatter(*self.start_point, color='green', s=100, label='Start', depthshade=True)
        # Draw end point (Red)
        self.ax.scatter(*self.end_point, color='red', s=100, label='End', depthshade=True)

    def show(self):
        """Displays the 3D plot."""
        self.ax.legend()
        plt.show()
