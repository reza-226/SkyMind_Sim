# skymind_sim/core/drone.py

class Drone:
    """
    کلاسی برای نمایش وضعیت و رفتار یک پهپاد در شبیه‌سازی.
    """
    def __init__(self, start_point: tuple, battery: float = 100.0, speed: float = 1.0):
        """
        سازنده کلاس Drone.

        Args:
            start_point (tuple): مختصات اولیه پهپاد به صورت (x, y, z).
            battery (float, optional): میزان اولیه باتری. پیش‌فرض 100.0 است.
            speed (float, optional): سرعت پهپاد. پیش‌فرض 1.0 (یک واحد در هر گام) است.
        """
        # موقعیت فعلی پهپاد
        self.position = start_point
        
        # میزان باتری
        self.battery = battery
        
        # سرعت پهپاد
        self.speed = speed
        
        # وضعیت پهپاد (e.g., 'IDLE', 'FLYING', 'LANDED')
        self.status = 'IDLE'

        print(f"Drone initialized at position {self.position} with {self.battery}% battery.")

    def move_to(self, new_position: tuple):
        """
        پهپاد را به موقعیت جدید منتقل کرده و وضعیت آن را به‌روز می‌کند.
        در آینده می‌توان منطق مصرف باتری را اینجا اضافه کرد.

        Args:
            new_position (tuple): مختصات مقصد بعدی.
        """
        # در یک پیاده‌سازی واقعی، مصرف باتری بر اساس مسافت طی شده محاسبه می‌شود.
        # distance = ((new_position[0] - self.position[0])**2 + ...)**0.5
        # self.battery -= distance * 0.1 # مثال: مصرف باتری
        
        self.position = new_position
        self.status = 'FLYING'
        # print(f"Drone moved to {self.position}") # این خط را کامنت می‌کنیم تا خروجی شلوغ نشود

    def get_status(self) -> dict:
        """
        وضعیت فعلی پهپاد را به صورت یک دیکشنری برمی‌گرداند.

        Returns:
            dict: دیکشنری شامل موقعیت، باتری و وضعیت پهپاد.
        """
        return {
            'position': self.position,
            'battery': self.battery,
            'status': self.status
        }
