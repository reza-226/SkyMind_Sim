# ============================================
# D:\Payannameh\SkyMind_Sim\skymind_sim\layer_1_simulation\world\world.py
# ============================================

class World:
    def __init__(self, grid_map, obstacles):
        self.grid_map = grid_map
        self.obstacles = obstacles

    def check_collision(self, position):
        return position in self.obstacles
