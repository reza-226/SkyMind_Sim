# skymind_sim/utils/singleton.py

import threading

class Singleton(type):
    """
    این یک Metaclass برای پیاده‌سازی الگوی طراحی Singleton است.
    هر کلاسی که از این Metaclass استفاده کند، تضمین می‌کند که تنها یک نمونه
    (instance) از آن در طول اجرای برنامه وجود خواهد داشت.
    
    این الگو برای کلاس‌هایی مانند ConfigLoader و LogManager مفید است
    تا از هر جای برنامه به یک نمونه واحد و ثابت دسترسی داشته باشیم.
    """
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """
        این متد زمانی فراخوانی می‌شود که شما سعی در ایجاد یک نمونه از کلاس دارید
        (مثلاً با فراخوانی ConfigLoader()).
        """
        # استفاده از lock برای جلوگیری از مشکلات در برنامه‌های چندنخی (thread-safe)
        with cls._lock:
            # اگر نمونه‌ای از این کلاس قبلاً ساخته نشده باشد، یکی جدید بساز
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        
        # نمونه موجود (یا تازه ساخته شده) را برگردان
        return cls._instances[cls]
