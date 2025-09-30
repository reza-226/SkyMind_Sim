# skymind_sim/core/scheduler.py

import heapq
from typing import List, Optional

from .event import Event

class Scheduler:
    """
    زمان‌بند مبتنی بر صف اولویت برای مدیریت رویدادهای شبیه‌سازی.

    این کلاس از ماژول heapq برای نگهداری یک صف از رویدادها استفاده می‌کند
    که بر اساس زمان وقوع (timestamp) مرتب شده‌اند.
    """
    def __init__(self):
        """
        سازنده کلاس Scheduler.
        یک صف رویداد خالی و زمان شبیه‌سازی اولیه را مقداردهی می‌کند.
        """
        self._event_queue: List[Event] = []
        self._current_time: float = 0.0

    @property
    def current_time(self) -> float:
        """زمان فعلی شبیه‌سازی را برمی‌گرداند."""
        return self._current_time

    def schedule_event(self, event: Event):
        """
        یک رویداد جدید را به صف اضافه می‌کند.

        Args:
            event (Event): رویدادی که باید زمان‌بندی شود.
        """
        heapq.heappush(self._event_queue, event)

    def get_next_event(self) -> Optional[Event]:
        """
        رویداد بعدی را از صف برداشته و زمان شبیه‌سازی را به‌روز می‌کند.

        اگر صفی خالی باشد، None را برمی‌گرداند.

        Returns:
            Optional[Event]: رویداد بعدی که باید پردازش شود یا None.
        """
        if not self._event_queue:
            return None

        next_event = heapq.heappop(self._event_queue)
        
        # اطمینان حاصل می‌کند که زمان به عقب برنمی‌گردد
        if next_event.timestamp < self._current_time:
            # این حالت نباید در یک شبیه‌سازی عادی رخ دهد
            # اما برای جلوگیری از خطاهای منطقی، زمان را به جلو می‌بریم
            print(f"Warning: Event {next_event.event_type} scheduled in the past. "
                  f"Event time: {next_event.timestamp}, Current time: {self._current_time}")
            # با این حال، زمان شبیه‌سازی را به زمان رویداد تغییر نمی‌دهیم
        
        self._current_time = next_event.timestamp
        return next_event

    def is_empty(self) -> bool:
        """
        بررسی می‌کند که آیا رویداد دیگری در صف وجود دارد یا خیر.

        Returns:
            bool: True اگر صف خالی باشد، در غیر این صورت False.
        """
        return not bool(self._event_queue)
