import configparser
import os
import logging

class Config:
    """
    Manages application configuration from a .ini file.
    
    [MODIFIED] Specified UTF-8 encoding when reading the config file
               to prevent UnicodeDecodeError.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_file='config.ini'):
        if not hasattr(self, '_config'):  # Prevent re-initialization
            self._config = configparser.ConfigParser()
            if not os.path.exists(config_file):
                raise FileNotFoundError(f"Configuration file not found: {config_file}")
            
            # --- MODIFICATION IS HERE ---
            # Read the file explicitly with UTF-8 encoding
            try:
                self._config.read(config_file, encoding='utf-8')
                logging.info(f"Configuration loaded from {config_file}")
            except Exception as e:
                logging.error(f"Failed to read or parse config file {config_file}: {e}")
                raise
            
            # --- Dynamically set project paths ---
            self.PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.DATA_DIR = os.path.join(self.PROJECT_ROOT, 'data')
            self.LOGS_DIR = os.path.join(self.DATA_DIR, 'simulation_logs')
            self.MAPS_DIR = os.path.join(self.DATA_DIR, 'maps')

    def get(self, section, option, fallback=None):
        """Gets a single value from a section."""
        if not isinstance(option, str):
            raise TypeError(f"The 'option' argument must be a string, not {type(option).__name__}.")
        return self._config.get(section, option, fallback=fallback)

    def get_section(self, section):
        """
        Retrieves an entire section from the config file as a dictionary.
        Returns an empty dictionary if the section does not exist.
        """
        if self._config.has_section(section):
            return dict(self._config.items(section))
        return {}

    def getboolean(self, section, option, fallback=False):
        """Gets a boolean value from a section."""
        return self._config.getboolean(section, option, fallback=fallback)

    def getint(self, section, option, fallback=0):
        """Gets an integer value from a section."""
        return self._config.getint(section, option, fallback=fallback)

    def getfloat(self, section, option, fallback=0.0):
        """Gets a float value from a section."""
        return self._config.getfloat(section, option, fallback=fallback)
