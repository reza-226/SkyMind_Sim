# skymind_sim/main.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from skymind_sim.core.environment import Environment
from skymind_sim.core.drone import Drone
from skymind_sim.core.simulation import Simulation

def setup_environment_with_obstacles():
    """
    محیط شبیه‌سازی را با پهپادها و موانع ایجاد و پیکربندی می‌کند.
    """
    # ایجاد محیط
    dimensions = np.array([500, 500, 100])
    environment = Environment(dimensions=dimensions)
    
    # ایجاد و افزودن پهپادها
    drone1 = Drone(drone_id="d1", initial_position=np.array([10.0, 10.0, 50.0]))
    drone2 = Drone(drone_id="d2", initial_position=np.array([490.0, 490.0, 70.0]))
    
    # تنظیم مسیر حرکتی برای پهپادها
    path1 = [np.array([450.0, 450.0, 60.0]), np.array([10.0, 10.0, 50.0])]
    path2 = [np.array([50.0, 50.0, 80.0]), np.array([490.0, 490.0, 70.0])]
    drone1.set_movement_path(path1)
    drone2.set_movement_path(path2)
    
    environment.add_drone(drone1)
    environment.add_drone(drone2)
    
    # ایجاد و افزودن موانع
    obstacle1_center = np.array([250, 250, 50])
    obstacle1_radius = 40
    environment.add_obstacle(obstacle1_center, obstacle1_radius)
    
    obstacle2_center = np.array([100, 400, 80])
    obstacle2_radius = 30
    environment.add_obstacle(obstacle2_center, obstacle2_radius)
    
    print(f"محیط ایجاد شد: {environment}")
    return environment

def run_simulation():
    """
    شبیه‌سازی را اجرا کرده و نتایج را به صورت بصری نمایش می‌دهد.
    """
    environment = setup_environment_with_obstacles()
    simulation = Simulation(environment=environment, total_time=200, time_step=0.5)

    # --- تنظیمات بصری‌سازی ---
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # رسم موانع (فقط یک بار در ابتدا)
    for obs in environment.obstacles:
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = obs['radius'] * np.outer(np.cos(u), np.sin(v)) + obs['center'][0]
        y = obs['radius'] * np.outer(np.sin(u), np.sin(v)) + obs['center'][1]
        z = obs['radius'] * np.outer(np.ones(np.size(u)), np.cos(v)) + obs['center'][2]
        ax.plot_surface(x, y, z, color='r', alpha=0.3)

    # نقاط اولیه پهپادها برای نمایش مسیر
    paths = {drone.drone_id: [drone.initial_position] for drone in environment.drones}
    
    # ایجاد scatter plot برای پهپادها (این plot در هر فریم آپدیت می‌شود)
    # موقعیت‌های اولیه را به عنوان داده اولیه می‌دهیم
    initial_positions = np.array([d.position for d in environment.drones])
    scatter = ax.scatter(initial_positions[:, 0], initial_positions[:, 1], initial_positions[:, 2], color='b', s=50, label="Drones")
    
    # ایجاد plot برای مسیرها
    path_plots = {drone.drone_id: ax.plot([], [], [], color='gray', linestyle='--', alpha=0.7)[0] for drone in environment.drones}

    def update(frame):
        # اجرای یک گام از شبیه‌سازی
        simulation.run_step()
        
        # دریافت موقعیت‌های جدید
        positions = simulation.get_current_positions()
        
        # بررسی برخورد با موانع
        collisions = environment.check_collisions()
        if collisions:
            for collision in collisions:
                print(f"Collision Detected! Time: {simulation.current_time:.2f}s, Drone: {collision['drone_id']}, Obstacle: {collision['obstacle_index']}")

        # به‌روزرسانی داده‌های scatter plot
        pos_array = np.array(list(positions.values()))
        scatter._offsets3d = (pos_array[:, 0], pos_array[:, 1], pos_array[:, 2])

        # به‌روزرسانی مسیرها
        for drone_id, pos in positions.items():
            paths[drone_id].append(pos)
            path_data = np.array(paths[drone_id])
            path_plots[drone_id].set_data(path_data[:, 0], path_data[:, 1])
            path_plots[drone_id].set_3d_properties(path_data[:, 2])

        # به‌روزرسانی عنوان اصلی فیگور برای نمایش زمان
        fig.suptitle(f"SkyMind Simulation | Time: {simulation.current_time:.2f}s", fontsize=14)

        return scatter, *path_plots.values()

    # تنظیمات محورها و لیبل‌ها
    ax.set_xlim(0, environment.dimensions[0])
    ax.set_ylim(0, environment.dimensions[1])
    ax.set_zlim(0, environment.dimensions[2])
    ax.set_xlabel("X (meters)")
    ax.set_ylabel("Y (meters)")
    ax.set_zlabel("Z (meters)")
    ax.legend()
    ax.grid(True)

    # ایجاد و اجرای انیمیشن
    # frames: تعداد کل فریم‌ها برای اجرا. interval: زمان بین فریم‌ها بر حسب میلی‌ثانیه.
    ani = FuncAnimation(fig, update, frames=int(simulation.total_time / simulation.time_step), 
                        interval=50, blit=False)
                        
    plt.show()

if __name__ == "__main__":
    run_simulation()
