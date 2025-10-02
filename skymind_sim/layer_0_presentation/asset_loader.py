# skymind_sim/layer_0_presentation/asset_loader.py
import pygame
import os

# پیدا کردن مسیر ریشه پروژه برای دسترسی به پوشه assets
# این کد از محل فایل asset_loader.py دو مرحله به بالا می‌رود (از layer_0_presentation به skymind_sim و سپس به ریشه پروژه)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

class AssetLoader:
    def __init__(self):
        self.images = {}
        self.fonts = {}
        # اطمینان از اینکه ماژول فونت Pygame مقداردهی اولیه شده است
        if not pygame.font.get_init():
            pygame.font.init()
        print("AssetLoader Singleton Initialized.")

    def get_path(self, asset_type: str, filename: str) -> str:
        """مسیر کامل یک asset را بر اساس نوع آن (images, fonts) می‌سازد."""
        return os.path.join(PROJECT_ROOT, 'assets', asset_type, filename)

    def load_image(self, filename: str) -> pygame.Surface:
        """یک تصویر را بارگذاری و کش می‌کند. در صورت خطا، یک سطح جایگزین برمی‌گرداند."""
        if filename not in self.images:
            full_path = self.get_path('images', filename)
            try:
                image = pygame.image.load(full_path).convert_alpha()
                self.images[filename] = image
                print(f"SUCCESS: Image loaded and cached from '{full_path}'")
            except pygame.error as e:
                print(f"ERROR: Cannot load image '{filename}'. Pygame error: {e}")
                # در صورت خطا یک مربع صورتی به عنوان جایگزین ایجاد می‌کنیم
                image = pygame.Surface((40, 40))
                image.fill((255, 0, 255)) # رنگ صورتی نشانگر خطاست
                self.images[filename] = image
        # یک کپی از تصویر را برمی‌گردانیم تا تغییرات ناخواسته روی نسخه کش شده اعمال نشود
        return self.images[filename].copy()

    def load_font(self, filename: str, size: int) -> pygame.font.Font:
        """یک فونت را بارگذاری و کش می‌کند. در صورت خطا، فونت پیش‌فرض Pygame را برمی‌گرداند."""
        key = (filename, size)
        if key not in self.fonts:
            full_path = self.get_path('fonts', filename)
            try:
                font = pygame.font.Font(full_path, size)
                self.fonts[key] = font
                print(f"SUCCESS: Font '{filename}' loaded at size {size}")
            except (pygame.error, FileNotFoundError) as e:
                print(f"ERROR: Cannot load font '{filename}'. Error: {e}")
                # در صورت خطا از فونت پیش‌فرض استفاده می‌کنیم
                font = pygame.font.Font(None, size)
                self.fonts[key] = font
        return self.fonts[key]

# =========================================================================
# >> نکته کلیدی اینجاست <<
# ما یک نمونه (instance) از کلاس AssetLoader با نام asset_loader ایجاد می‌کنیم.
# فایل‌های دیگر (مثل renderer.py) همین نمونه را import خواهند کرد.
# =========================================================================
asset_loader = AssetLoader()
