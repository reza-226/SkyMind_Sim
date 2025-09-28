# run_and_visualize.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

from skymind_sim.core.drone import Drone, DroneStatus
from skymind_sim.core.environment import Environment
from skymind_sim.core.simulation import Simulation

def setup_scenario():
    """یک سناریو با پهپادهای هوشمند که به سمت مقصد حرکت می‌کنند."""
    env = Environment(width=200, height=200, depth=100)
    
    # پهپاد ۱: از یک گوشه به گوشه دیگر پرواز می‌کند
    drone1 = Drone(drone_id=1)
    drone1.move_to(np.array([10.0, 10.0, 10.0]))
    drone1.set_destination(np.array([180.0, 180.0, 60.0]), speed=15.0) # سرعت بالا
    
    # پهپاد ۲: یک مسیر کوتاه افقی را طی می‌کند
    drone2 = Drone(drone_id=2)
    drone2.move_to(np.array([100.0, 180.0, 80.0]))
    drone2.set_destination(np.array([100.0, 20.0, 80.0]), speed=10.0) # سرعت متوسط
    
    # پهپاد ۳: یک صعود عمودی انجام می‌دهد
    drone3 = Drone(drone_id=3)
    drone3.move_to(np.array([50.0, 50.0, 20.0]))
    drone3.set_destination(np.array([50.0, 50.0, 90.0]), speed=5.0) # سرعت کم
    
    # پهپاد ۴: از ابتدا بیکار است و حرکتی نمی‌کند
    drone4 = Drone(drone_id=4)
    drone4.move_to(np.array([150.0, 100.0, 50.0]))
    # چون مقصدی برایش تنظیم نمی‌کنیم، وضعیت آن FLYING نخواهد شد و ثابت می‌ماند
    drone4.status = DroneStatus.IDLE

    env.add_drone(drone1)
    env.add_drone(drone2)
    env.add_drone(drone3)
    env.add_drone(drone4)
    
    return env

def visualize_simulation_3d(simulation: Simulation):
    """
    یک انیمیشن سه‌بعدی از مسیر حرکت پهپادها ایجاد می‌کند.
    """
    history = simulation.history
    if not history:
        print("History is empty. Cannot visualize.")
        return

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim(0, simulation.environment.width)
    ax.set_ylim(0, simulation.environment.height)
    ax.set_zlim(0, simulation.environment.depth)
    ax.set_xlabel("X-axis (meters)")
    ax.set_ylabel("Y-axis (meters)")
    ax.set_zlabel("Z-axis (Height)")
    ax.set_title("3D Drone Simulation with Pathfinding")
    ax.invert_yaxis()

    paths = {}
    drone_ids_with_history = [drone_id for drone_id, states in history.items() if states]
    
    for drone_id in drone_ids_with_history:
        states = history[drone_id]
        times, xs, ys, zs = zip(*states)
        paths[drone_id] = (list(xs), list(ys), list(zs))

    path_plots = {}
    for drone_id, (xs, ys, zs) in paths.items():
        path_plots[drone_id] = ax.plot(xs, ys, zs, '--', alpha=0.4)[0]

    points = {drone_id: ax.plot([], [], [], 'o', markersize=6, label=f'Drone {drone_id}')[0] 
              for drone_id in drone_ids_with_history}
    
    def init():
        for point in points.values():
            point.set_data([], [])
            point.set_3d_properties([])
        return points.values()

    def update(frame):
        for drone_id, point in points.items():
            if frame < len(paths[drone_id][0]):
                x, y, z = paths[drone_id][0][frame], paths[drone_id][1][frame], paths[drone_id][2][frame]
                point.set_data([x], [y])
                point.set_3d_properties([z])
        return points.values()

    num_frames = max((len(s) for s in history.values() if s), default=0)
    ani = FuncAnimation(fig, update, frames=num_frames,
                        init_func=init, blit=False, interval=20, repeat=False)

    ax.legend()
    plt.show()

def main():
    """
    تابع اصلی برای تنظیم، اجرا و بصری‌سازی شبیه‌سازی.
    """
    env = setup_scenario()
    sim = Simulation(environment=env)
    # افزایش تعداد گام‌ها برای اطمینان از رسیدن پهپادها به مقصد
    sim.run(num_steps=200, dt=0.2)
    visualize_simulation_3d(sim)

if __name__ == "__main__":
    main()
