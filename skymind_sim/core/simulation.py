# skymind_sim/core/simulation.py

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# ایمپورت نسبی از ماژول هم‌سطح
from .drone import Drone

class Simulation:
    """کلاس برای اجرای و نمایش شبیه‌سازی."""
    def __init__(self, environment):
        self.env = environment
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.drone_artists = []
        self.path_artists = []
        self.history_artists = []
        self.drone_history = [[] for _ in self.env.drones]

    def _draw_obstacle(self, obstacle):
        """یک مانع مکعبی را در plot رسم می‌کند."""
        if not (hasattr(obstacle, 'min_corner') and hasattr(obstacle, 'max_corner')):
            return

        min_c, max_c = obstacle.min_corner, obstacle.max_corner
        
        # تعریف ۸ گوشه مکعب برای خوانایی بیشتر
        p0 = [min_c[0], min_c[1], min_c[2]]
        p1 = [max_c[0], min_c[1], min_c[2]]
        p2 = [max_c[0], max_c[1], min_c[2]]
        p3 = [min_c[0], max_c[1], min_c[2]]
        p4 = [min_c[0], min_c[1], max_c[2]]
        p5 = [max_c[0], min_c[1], max_c[2]]
        p6 = [max_c[0], max_c[1], max_c[2]]
        p7 = [min_c[0], max_c[1], max_c[2]]

        # رسم ۱۲ یال مکعب
        # کف مکعب
        self.ax.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]], 'r-')
        self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 'r-')
        self.ax.plot([p2[0], p3[0]], [p2[1], p3[1]], [p2[2], p3[2]], 'r-')
        self.ax.plot([p3[0], p0[0]], [p3[1], p0[1]], [p3[2], p0[2]], 'r-')

        # سقف مکعب
        self.ax.plot([p4[0], p5[0]], [p4[1], p5[1]], [p4[2], p5[2]], 'r-')
        self.ax.plot([p5[0], p6[0]], [p5[1], p6[1]], [p5[2], p6[2]], 'r-')
        self.ax.plot([p6[0], p7[0]], [p6[1], p7[1]], [p6[2], p7[2]], 'r-')
        self.ax.plot([p7[0], p4[0]], [p7[1], p4[1]], [p7[2], p4[2]], 'r-')

        # ستون‌های عمودی
        self.ax.plot([p0[0], p4[0]], [p0[1], p4[1]], [p0[2], p4[2]], 'r-')
        self.ax.plot([p1[0], p5[0]], [p1[1], p5[1]], [p1[2], p5[2]], 'r-')
        self.ax.plot([p2[0], p6[0]], [p2[1], p6[1]], [p2[2], p6[2]], 'r-')
        self.ax.plot([p3[0], p7[0]], [p3[1], p7[1]], [p3[2], p7[2]], 'r-')

    def _init_plot(self):
        """مقداردهی اولیه plot."""
        self.ax.set_xlim([0, self.env.dimensions[0]])
        self.ax.set_ylim([0, self.env.dimensions[1]])
        self.ax.set_zlim([0, self.env.dimensions[2]])
        self.ax.set_xlabel('X (m)')
        self.ax.set_ylabel('Y (m)')
        self.ax.set_zlabel('Z (m)')
        self.ax.set_title('SkyMind Drone Simulation - A* Pathfinding')
        self.ax.grid(True)

        # رسم موانع با استفاده از تابع کمکی
        for obs in self.env.obstacles:
            self._draw_obstacle(obs)

        # مقداردهی اولیه هنرمندان (artists) برای پهپادها و مسیرها
        colors = plt.cm.jet(np.linspace(0, 1, len(self.env.drones)))
        for i, drone in enumerate(self.env.drones):
            # نمایش پهپاد
            artist, = self.ax.plot([], [], [], 'o', color=colors[i], markersize=8, label=f'Drone {drone.id}')
            self.drone_artists.append(artist)
            
            # نمایش مسیر برنامه‌ریزی شده
            if drone.path:
                path_points = np.array(drone.path)
                path_artist, = self.ax.plot(path_points[:, 0], path_points[:, 1], path_points[:, 2], '--', color=colors[i], alpha=0.5)
                self.path_artists.append(path_artist)
            
            # نمایش مسیر طی شده
            history_artist, = self.ax.plot([], [], [], '-', color=colors[i], linewidth=2)
            self.history_artists.append(history_artist)

        self.ax.legend()
        return self.drone_artists + self.history_artists

    def _update_plot(self, frame):
        """به‌روزرسانی plot در هر فریم."""
        # به‌روزرسانی منطق شبیه‌سازی
        dt = 0.1  # گام زمانی
        self.env.update(dt)

        # به‌روزرسانی نمایش
        for i, drone in enumerate(self.env.drones):
            pos = drone.position
            
            # set_data و set_3d_properties برای هنرمندان انتظار دنباله (sequence) دارند.
            # حتی برای یک نقطه، باید آن را در یک لیست یا آرایه تک‌عضوی قرار دهیم.
            self.drone_artists[i].set_data([pos[0]], [pos[1]])
            self.drone_artists[i].set_3d_properties([pos[2]])
            
            # به‌روزرسانی مسیر طی شده
            self.drone_history[i].append(drone.get_history_point())
            # برای جلوگیری از خطای احتمالی در فریم اول اگر هیستوری خالی باشد
            if self.drone_history[i]:
                hist_array = np.array(self.drone_history[i])
                # مطمئن می‌شویم که hist_array خالی نیست و دو بعدی است
                if hist_array.ndim == 2 and hist_array.shape[0] > 0: 
                    self.history_artists[i].set_data(hist_array[:, 0], hist_array[:, 1])
                    self.history_artists[i].set_3d_properties(hist_array[:, 2])

        return self.drone_artists + self.history_artists

    def run(self):
        """اجرای شبیه‌سازی."""
        # با توجه به مشکلات احتمالی blitting در برخی سیستم‌ها، آن را False می‌کنیم.
        # blit=False پایدارتر است و از خطاهای رندرینگ جلوگیری می‌کند.
        ani = FuncAnimation(self.fig, self._update_plot, init_func=self._init_plot,
                              frames=200, interval=50, blit=False)
        plt.show()
