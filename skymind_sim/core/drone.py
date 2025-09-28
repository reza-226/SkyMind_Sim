# skymind_sim/core/drone.py

from enum import Enum, auto
import numpy as np

class DroneStatus(Enum):
    """وضعیت‌های ممکن برای یک پهپاد."""
    IDLE = auto()      # بیکار و ثابت
    FLYING = auto()    # در حال پرواز به سمت مقصد
    HOVERING = auto()  # شناور در یک نقطه (مثلاً پس از رسیدن به مقصد)
    ERROR = auto()     # وضعیت خطا

class Drone:
    """
    نشان‌دهنده یک پهپاد در شبیه‌سازی.
    
    Attributes:
        drone_id (int): شناسه منحصر به فرد پهپاد.
        position (np.ndarray): موقعیت فعلی پهپاد [x, y, z].
        velocity (np.ndarray): سرعت فعلی پهپاد [vx, vy, vz].
        status (DroneStatus): وضعیت فعلی پهپاد.
        destination (np.ndarray | None): موقعیت مقصد [x, y, z].
        target_speed (float): سرعت مطلوب برای حرکت به سمت مقصد (متر بر ثانیه).
    """
    
    def __init__(self, drone_id: int):
        self.drone_id = drone_id
        self.position = np.zeros(3, dtype=float)
        self.velocity = np.zeros(3, dtype=float)
        self.status = DroneStatus.IDLE
        
        # ویژگی‌های جدید برای هدایت خودکار
        self.destination: np.ndarray | None = None
        self.target_speed: float = 5.0 # سرعت پیش‌فرض: 5 متر بر ثانیه

    def move_to(self, position: np.ndarray):
        """موقعیت پهپاد را فوراً به یک نقطه جدید منتقل می‌کند."""
        self.position = np.array(position, dtype=float)

    def set_velocity(self, velocity: np.ndarray):
        """سرعت پهپاد را به صورت دستی تنظیم می‌کند."""
        self.velocity = np.array(velocity, dtype=float)
        
    def set_destination(self, destination: np.ndarray, speed: float = 5.0):
        """
        یک مقصد برای پهپاد تعیین می‌کند و وضعیت آن را برای پرواز آماده می‌کند.
        """
        self.destination = np.array(destination, dtype=float)
        self.target_speed = speed
        self.status = DroneStatus.FLYING # با تنظیم مقصد، پهپاد آماده پرواز می‌شود
