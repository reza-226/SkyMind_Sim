# skymind_sim/config.py

import logging

# ==============================================================================
# Simulation Configuration
# ==============================================================================
# This dictionary holds all the core settings for the simulation window,
# frame rate, and other general parameters.
SIMULATION_CONFIG = {
    # Window and Rendering settings
    'window_width': 1280,
    'window_height': 720,
    'fps_limit': 60,

    # Colors used in the renderer
    'colors': {
        'background': (30, 30, 30),      # Dark Gray
        'obstacle': (100, 100, 100),    # Gray
        'drone_trail': (0, 150, 255),     # Blue
        'text': (240, 240, 240)           # Light Gray
    },
    
    # Asset paths (relative to the asset_loader root)
    'assets': {
        'drone_image': 'drone.png',
        'main_font': 'Roboto-Regular.ttf'
    }
}


# ==============================================================================
# Logging Configuration
# ==============================================================================
# Centralized configuration for the logging system.
LOGGING_CONFIG = {
    'level': logging.DEBUG,  # Set the minimum level of messages to log
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
    'log_file': 'data/simulation_logs/sim_run.log' # Path to the log file
}


# ==============================================================================
# Drone Default Configuration
# ==============================================================================
# Default parameters for creating a new drone.
DRONE_CONFIG = {
    'default_speed': 150.0,  # pixels per second
    'battery_capacity': 100.0, # Wh (Watt-hours)
    'energy_consumption_rate': 0.1 # Wh per second (at idle/hover)
}
