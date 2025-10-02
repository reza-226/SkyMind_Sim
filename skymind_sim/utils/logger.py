import logging
import os
from datetime import datetime

def setup_logging():
    """Configures the logging for the application."""
    log_dir = "data/simulation_logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_filename = datetime.now().strftime("simulation_%Y%m%d_%H%M%S.log")
    log_filepath = os.path.join(log_dir, log_filename)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filepath),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging configured successfully.")
    logging.info(f"Log file created at: {log_filepath}")
