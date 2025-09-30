# skymind_sim/core/environment.py

import numpy as np

class Environment:
    """
    کلاسی برای مدیریت محیط شبیه‌سازی، شامل نقشه، ابعاد و موانع.
    این کلاس داده‌های نقشه را به صورت دیکشنری دریافت کرده و محیط را برای
    شبیه‌سازی و مسیریابی آماده می‌کند.
    """
    def __init__(self, map_data: dict):
        """
        سازنده کلاس Environment.

        Args:
            map_data (dict): یک دیکشنری حاوی داده‌های نقشه که از فایل JSON بارگذاری شده.
        """
        print(f"Initializing Environment with map: {map_data}\n")
        try:
            # مرحله 1: ذخیره داده‌های خام نقشه
            self.map_data = map_data
            
            # مرحله 2: استخراج ابعاد محیط
            # ابعاد به صورت (width, depth, height) یا (x_max, y_max, z_max)
            dims = self.map_data['dimensions']
            self.dimensions = (dims[0], dims[1], dims[2])

            # مرحله 3: پردازش و ساخت موانع
            # self.obstacles مجموعه‌ای از تمام نقاط (x,y,z) است که توسط موانع اشغال شده‌اند.
            self.obstacles = self._create_obstacles()
            print(f"Obstacles created. Total obstacle points: {len(self.obstacles)}")

        except (KeyError, IndexError) as e:
            # اگر کلیدهای ضروری در دیکشنری نقشه وجود نداشته باشند
            raise ValueError(f"Map data is missing required key or is malformed: {e}")
        except Exception as e:
            # برای سایر خطاهای غیرمنتظره
            raise Exception(f"Failed to initialize environment: {e}")

    def _create_obstacles(self) -> set:
        """
        موانع را از داده‌های نقشه خوانده و آن‌ها را به مجموعه‌ای از نقاط اشغال‌شده تبدیل می‌کند.
        در حال حاضر فقط از موانع مکعبی (cuboid) پشتیبانی می‌شود.
        """
        obstacle_points = set()
        if 'obstacles' not in self.map_data:
            return obstacle_points # اگر هیچ مانعی تعریف نشده باشد

        for obs_data in self.map_data['obstacles']:
            if obs_data['type'] == 'cuboid':
                pos = np.array(obs_data['position'])
                size = np.array(obs_data['size'])
                
                # گوشه شروع و پایان مکعب را مشخص کنید
                start_corner = pos
                end_corner = pos + size
                
                # تمام نقاط صحیح داخل این مکعب را به مجموعه موانع اضافه کنید
                for x in range(start_corner[0], end_corner[0]):
                    for y in range(start_corner[1], end_corner[1]):
                        for z in range(start_corner[2], end_corner[2]):
                            obstacle_points.add((x, y, z))
        
        return obstacle_points

    def is_valid_point(self, point: tuple) -> bool:
        """
        بررسی می‌کند که آیا یک نقطه در محدوده محیط قرار دارد و با هیچ مانعی برخورد نمی‌کند.

        Args:
            point (tuple): مختصات (x, y, z) نقطه مورد نظر.

        Returns:
            bool: True اگر نقطه معتبر باشد، در غیر این صورت False.
        """
        x, y, z = point
        width, depth, height = self.dimensions

        # 1. بررسی مرزهای محیط
        if not (0 <= x < width and 0 <= y < depth and 0 <= z < height):
            return False
        
        # 2. بررسی برخورد با موانع
        if point in self.obstacles:
            return False
            
        return True
