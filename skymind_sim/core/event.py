# skymind_sim/core/event.py

from dataclasses import dataclass, field
from typing import Any, Callable

@dataclass(order=True)
class Event:
    """
    نشان‌دهنده یک رویداد در شبیه‌سازی است.

    این کلاس از dataclass(order=True) استفاده می‌کند تا رویدادها
    به طور خودکار بر اساس زمان وقوع (timestamp) قابل مرتب‌سازی باشند.
    این ویژگی برای صف اولویت (priority queue) بسیار حیاتی است.

    Attributes:
        timestamp (float): زمان وقوع رویداد در شبیه‌سازی.
        priority (int): اولویت رویداد. عدد کمتر به معنای اولویت بالاتر است.
                         برای رویدادهایی که در یک زمان یکسان رخ می‌دهند استفاده می‌شود.
        action (Callable): تابعی (یا متدی) که باید هنگام پردازش رویداد فراخوانی شود.
        event_type (str): یک رشته برای توصیف نوع رویداد (مثلاً 'DRONE_UPDATE').
        data (Any): داده‌های اضافی مرتبط با رویداد که به تابع action پاس داده می‌شود.
    """
    timestamp: float
    priority: int
    # 'action' نباید در مقایسه برای مرتب‌سازی شرکت کند، چون قابل مقایسه نیست.
    # از field برای این کار استفاده می‌کنیم.
    action: Callable = field(compare=False) 
    event_type: str = field(compare=False)
    data: Any = field(default=None, compare=False)
