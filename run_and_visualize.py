# run_and_visualize.py
import pygame
from skymind_sim.utils.logger import LogManager
from skymind_sim.layer_1_simulation.simulation import Simulation
from skymind_sim.layer_0_presentation.renderer import PygameRenderer

def main():
    # 1. راه اندازی Logger اصلی با استفاده از get_logger
    main_logger = LogManager.get_logger("MainRunner")
    main_logger.info("Application starting...")

    try:
        # 2. راه اندازی شبیه‌ساز (دیگر به آن لاگر پاس نمی‌دهیم)
        map_path = "data/maps/simple_map.json"
        main_logger.info(f"Initializing Simulation with map: {map_path}")
        sim = Simulation(map_filename=map_path) # فراخوانی اصلاح شد

        # 3. دریافت ابعاد گرید از شبیه‌ساز
        grid_width, grid_height = sim.grid_dimensions
        
        # 4. راه اندازی رندرکننده
        main_logger.info(f"Initializing PygameRenderer with grid dimensions: {grid_width}x{grid_height}")
        renderer = PygameRenderer(
            grid_width=grid_width, 
            grid_height=grid_height,
            # لاگر رندرکننده را هم مستقیم از LogManager می‌گیریم
            logger=LogManager.get_logger("Renderer") 
        )

        # 5. حلقه اصلی برنامه
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
            
            sim.run_step()
            world_state = sim.get_world_state()
            renderer.render(world_state)

        # 6. پایان کار
        main_logger.info("Closing Pygame window.")
        renderer.close()

    except Exception as e:
        main_logger.critical(f"An unexpected error occurred: {e}", exc_info=True)
    finally:
        main_logger.info("Application finished gracefully.")
        pygame.quit()

if __name__ == "__main__":
    main()
