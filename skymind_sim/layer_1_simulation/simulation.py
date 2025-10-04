# مسیر: skymind_sim/layer_1_simulation/simulation.py
import pygame
import logging
from skymind_sim.layer_0_presentation.environment import Environment
from skymind_sim.layer_0_presentation.renderer import Renderer
from skymind_sim.layer_1_simulation.scheduler import Scheduler
from skymind_sim.utils.logger import setup_logging
from skymind_sim.utils.config_loader import load_json_config  # ← اصلاح این خط

class Simulation:
    def __init__(self, map_data, drone_configs, simulation_config):
        setup_logging(level="INFO", log_file="data/simulation_logs/simulation.log")
        self.logger = logging.getLogger("SkyMind")
        self.logger.info("Initializing Simulation...")

        # به جای load_config استفاده از load_json_config
        self.window_config = load_json_config("data/config/window.json")
        self.grid_config = load_json_config("data/config/grid.json")
        self.simulation_config = simulation_config

        self.environment = Environment(self.window_config, self.grid_config, self.simulation_config)
        self.renderer = Renderer(self.environment)
        self.scheduler = Scheduler(self.environment, self.simulation_config)

        self.logger.info("Environment & Renderer initialized successfully.")

    def run(self):
        self.logger.info("Simulation run started...")
        pygame.init()
        clock = pygame.time.Clock()

        while not self.scheduler.is_finished():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                    return

            self.scheduler.update()
            self.renderer.render_frame()
            clock.tick(60)

        self.logger.info("Simulation run finished.")
        pygame.quit()

    def stop(self):
        self.logger.info("Stopping simulation...")
        self.scheduler.stop()
        self.logger.info("Simulation stopped.")
