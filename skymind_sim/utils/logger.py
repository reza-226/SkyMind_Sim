# skymind_sim/utils/logger.py
import logging
import os
from datetime import datetime

# مقدار پیش‌فرض سطح لاگ را به INFO تغییر می‌دهیم تا با کد قبلی سازگارتر باشد
def setup_logging(log_level: int = logging.INFO):
    """
    Configures the logging for the application.
    Accepts a log_level to be set.
    """
    log_dir = "data/simulation_logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_filename = datetime.now().strftime("simulation_%Y%m%d_%H%M%S.log")
    log_filepath = os.path.join(log_dir, log_filename)

    # پاک کردن handler های قبلی برای جلوگیری از لاگ تکراری
    # این خط مهم است اگر تابع setup_logging ممکن است چند بار فراخوانی شود
    logging.getLogger().handlers = []

    logging.basicConfig(
        # از پارامتر ورودی برای تنظیم سطح لاگ استفاده می‌کنیم
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filepath),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging configured successfully.")
    logging.info(f"Log file created at: {log_filepath}")
    logging.info(f"Logging level set to: {logging.getLevelName(log_level)}")
