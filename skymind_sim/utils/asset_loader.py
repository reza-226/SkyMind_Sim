# FILE: skymind_sim/utils/asset_loader.py

import os
import pygame

class AssetLoader:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AssetLoader, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def initialize(self):
        if self._initialized:
            return
        
        print("Initializing AssetLoader...")
        
        # محاسبه مسیرها
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.data_path = os.path.join(self.base_path, 'data')
        self.font_path = os.path.join(self.data_path, 'fonts')
        self.image_path = os.path.join(self.data_path, 'images')

        # دیکشنری برای نگهداری منابع
        self.fonts = {}
        self.images = {}

        # بارگذاری همه منابع
        self._load_fonts()
        self._load_images()

        self._initialized = True
        print("AssetLoader initialized successfully.")

    def _load_fonts(self):
        """تمام فونت‌ها را بارگذاری می‌کند."""
        self.fonts['technical_small'] = self._load_font_file('Roboto-Regular.ttf', 12)
        print("Fonts loaded.")

    def _load_font_file(self, filename, size):
        """یک فایل فونت را بارگذاری می‌کند."""
        path = os.path.join(self.font_path, filename)
        try:
            return pygame.font.Font(path, size)
        except pygame.error:
            print(f"Warning: Font '{filename}' not found. Using default font.")
            return pygame.font.Font(None, size)

    def _load_images(self):
        """تمام تصاویر را بارگذاری می‌کند."""
        DRONE_ICON_SIZE = (35, 35)
        # --- DEBUGGING SECTION ---
        image_filename = 'drone_icon.png'
        full_path = os.path.join(self.image_path, image_filename)
        print(f"\n--- DEBUG: Checking for image at: '{full_path}'")
        if os.path.exists(full_path):
            print("--- DEBUG: File FOUND. Attempting to load...")
        else:
            print("--- DEBUG: File NOT FOUND! This will cause an error.")
            # برای اطمینان، محتوای پوشه را لیست می‌کنیم
            if os.path.exists(self.image_path):
                 print(f"--- DEBUG: Contents of '{self.image_path}': {os.listdir(self.image_path)}")
            else:
                 print(f"--- DEBUG: Directory '{self.image_path}' does not exist.")
        # --- END DEBUGGING ---
        self.images['drone_default'] = self._load_image_file(image_filename, DRONE_ICON_SIZE)
        if self.images.get('drone_default'):
            print("Image 'drone_default' loaded successfully.")

    def _load_image_file(self, filename, size=None):
        """یک فایل تصویر را با قابلیت تغییر اندازه بارگذاری می‌کند."""
        path = os.path.join(self.image_path, filename)
        try:
            image = pygame.image.load(path).convert_alpha()
            if size:
                image = pygame.transform.scale(image, size)
            return image
        except pygame.error as e:
            # خطا را با اطلاعات بیشتر دوباره ایجاد می‌کنیم تا دقیقاً بدانیم مشکل چیست
            raise FileNotFoundError(f"Failed to load image at '{path}'. Original pygame error: {e}")

# تابع جهانی برای دسترسی به نمونه Singleton
def get_asset_loader():
    return AssetLoader()
