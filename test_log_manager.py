# test_log_manager.py (نسخه اصلاح شده)

import unittest
import logging
import os
from pathlib import Path

# ابتدا مطمئن شوید که مسیر پروژه در sys.path قرار دارد تا بتوانیم ماژول‌ها را ایمپورت کنیم
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

from skymind_sim.utils.log_manager import LogManager, get_logger
from skymind_sim.utils.config_loader import ConfigLoader

class TestLogManager(unittest.TestCase):

    def setUp(self):
        """این متد قبل از هر تست اجرا می‌شود"""
        # ما نیاز داریم که قبل از هر تست، Singleton ها را ریست کنیم
        # تا تست‌ها از هم مستقل باشند.
        LogManager._instance = None
        ConfigLoader._instance = None
        
        # --- START: تغییرات اعمال شده ---
        # 1. یک نمونه از ConfigLoader بگیرید
        self.config = ConfigLoader()
        
        # 2. به آن بگویید فایل‌های پیکربندی را بارگذاری کند
        #    این همان مرحله‌ای است که فراموش شده بود.
        #    ما مسیر پوشه کانفیگ را به صورت نسبی به فایل تست می‌دهیم.
        config_dir = Path(__file__).resolve().parent / "data" / "config"
        self.config.load_from_directory(config_dir)
        # --- END: تغییرات اعمال شده ---
        
        # مسیر فایل لاگ تست را مشخص می‌کنیم
        # حالا این خط بدون خطا اجرا خواهد شد
        self.log_file_path = Path(self.config.get('logging.log_file', 'test.log'))

        # اگر فایل لاگ از تست قبلی باقی مانده، آن را حذف می‌کنیم
        if self.log_file_path.exists():
            root_logger = logging.getLogger()
            for handler in root_logger.handlers[:]:
                handler.close()
                root_logger.removeHandler(handler)
            os.remove(self.log_file_path)

    def test_singleton_pattern(self):
        """تست می‌کند که LogManager یک Singleton است"""
        print("\n--- Testing Singleton Pattern ---")
        lm1 = LogManager()
        lm2 = LogManager()
        self.assertIs(lm1, lm2, "LogManager should be a Singleton")
        print("✅ Singleton test passed.")

    def test_logger_creation_and_logging(self):
        """تست می‌کند که لاگر به درستی ایجاد و پیام‌ها ثبت می‌شوند"""
        print("\n--- Testing Logger Creation and Logging ---")
        
        # مقداردهی اولیه LogManager (اگر قبلا نشده باشد)
        # حالا LogManager در داخل خود می‌تواند با موفقیت از ConfigLoader استفاده کند
        log_manager = LogManager()
        
        # گرفتن یک لاگر
        logger = get_logger("TestLogger")
        self.assertIsInstance(logger, logging.Logger, "get_logger should return a Logger instance")
        
        # ثبت چند پیام تست
        test_message_info = "This is an info test message."
        test_message_debug = "This is a debug test message."
        logger.info(test_message_info)
        logger.debug(test_message_debug)
        print("Logged messages to file and console.")
        
        # بررسی محتوای فایل لاگ
        self.assertTrue(self.log_file_path.exists(), "Log file should be created.")
        
        with open(self.log_file_path, 'r') as f:
            log_content = f.read()
            
        # بر اساس logging.json، پیام INFO باید در فایل باشد
        self.assertIn(test_message_info, log_content, "INFO message should be in the log file.")
        
        # بر اساس logging.json، پیام DEBUG نباید در فایل باشد (چون level فایل INFO است)
        self.assertNotIn(test_message_debug, log_content, "DEBUG message should NOT be in the log file.")
        
        print("✅ Log file content verified successfully.")

    def tearDown(self):
        """این متد بعد از هر تست اجرا می‌شود"""
        # پاکسازی فایل لاگ بعد از اتمام تست
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            handler.close()
            root_logger.removeHandler(handler)
        if self.log_file_path.exists():
            try:
                os.remove(self.log_file_path)
            except PermissionError:
                print(f"Warning: Could not remove log file {self.log_file_path}")


if __name__ == '__main__':
    print("--- Starting LogManager Test Suite ---")
    unittest.main(verbosity=0, exit=False)
    print("\n--- All LogManager tests passed successfully! ---")
