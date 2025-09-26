# skymind_sim/core/drone.py

from typing import Tuple, List, TYPE_CHECKING

# این بلوک برای جلوگیری از خطاهای واردات چرخه‌ای (circular import) است.
if TYPE_CHECKING:
    from .environment import Environment

class Drone:
    """
    کلاسی برای نمایش و مدیریت وضعیت یک پهپاد.
    """
    def __init__(self, drone_id: str, position: Tuple[int, int]):
        """
        سازنده کلاس پهپاد.
        
        :param drone_id: شناسه منحصر به فرد پهپاد.
        :param position: موقعیت اولیه پهپاد (row, col).
        """
        self.drone_id = drone_id
        self.position = position
        self.path: List[Tuple[int, int]] = []
        self.path_index = 0
        self.is_active = False # پهپاد تا زمانی که مسیر نداشته باشد فعال نیست
        self.env: 'Environment' = None

    def set_environment(self, env: 'Environment'):
        """
        محیطی که پهپاد در آن قرار دارد را تنظیم می‌کند.
        """
        self.env = env

    def set_path(self, path: List[Tuple[int, int]]):
        """
        مسیر حرکت پهپاد را تنظیم می‌کند.
        """
        self.path = path
        self.path_index = 0
        # اگر مسیر معتبر و دارای حداقل یک گام باشد، پهپاد فعال می‌شود
        if self.path and len(self.path) > 0:
            self.is_active = True
        else:
            self.is_active = False
            
    def follow_path(self):
        """
        پهپاد را یک گام در مسیر تعیین شده به جلو می‌برد.
        """
        if not self.is_active:
            return

        if self.path_index < len(self.path):
            # به موقعیت بعدی در مسیر حرکت کن
            self.position = self.path[self.path_index]
            self.path_index += 1
        
        if self.path_index >= len(self.path):
            self.is_active = False
            print(f"Drone {self.drone_id} has reached its destination at {self.position}.")

    def __repr__(self) -> str:
        return f"Drone(id='{self.drone_id}', pos={self.position})"
