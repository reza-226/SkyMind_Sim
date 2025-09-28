# skymind_sim/utils/visualizer.py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from collections import defaultdict

def plot_drone_paths(history: defaultdict):
    """
    Plots the 3D paths of all drones from the simulation history.

    Args:
        history (defaultdict): A dictionary where keys are drone_ids and
                               values are lists of (time, x, y, z) tuples.
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    if not history:
        print("History is empty. Nothing to plot.")
        ax.set_title("No Drone Data Available")
        plt.show()
        return

    # پیدا کردن محدوده نمودار برای تنظیم view
    all_x = []
    all_y = []
    all_z = []

    # برای هر پهپاد، مسیرش را رسم کن
    for drone_id, path in history.items():
        if not path:
            continue

        # جدا کردن داده‌های x, y, z از تاپل‌ها
        # path is a list of (time, x, y, z)
        times, x_coords, y_coords, z_coords = zip(*path)
        
        # اضافه کردن مختصات به لیست کلی برای تنظیم محدوده
        all_x.extend(x_coords)
        all_y.extend(y_coords)
        all_z.extend(z_coords)

        # رسم مسیر
        ax.plot(x_coords, y_coords, z_coords, marker='o', markersize=2, linestyle='-', label=f'Path {drone_id}')

        # مشخص کردن نقطه شروع و پایان
        ax.scatter(x_coords[0], y_coords[0], z_coords[0], c='green', s=100, marker='^', label=f'Start {drone_id}', depthshade=True)
        ax.scatter(x_coords[-1], y_coords[-1], z_coords[-1], c='red', s=100, marker='X', label=f'End {drone_id}', depthshade=True)

    # تنظیمات ظاهری نمودار
    ax.set_xlabel('X Coordinate (meters)')
    ax.set_ylabel('Y Coordinate (meters)')
    ax.set_zlabel('Z Coordinate (Altitude)')
    ax.set_title('3D Drone Trajectories')
    ax.legend()
    ax.grid(True)
    
    # تنظیم محدوده محورها برای نمایش بهتر همه مسیرها
    if all_x:
        ax.set_xlim(min(all_x) - 10, max(all_x) + 10)
        ax.set_ylim(min(all_y) - 10, max(all_y) + 10)
        ax.set_zlim(min(all_z) - 5, max(all_z) + 5)


    print("Displaying plot...")
    plt.show()
