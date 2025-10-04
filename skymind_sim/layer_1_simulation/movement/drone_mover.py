from skymind_sim.layer_3_intelligence.pathfinding.path_planner import PathPlanner
from skymind_sim.layer_1_simulation.world.world import World

class DroneMover:
    def __init__(self, world: World):
        # دادن موانع به پلنر
        self.world = world
        self.path_planner = PathPlanner(world.grid_map, obstacles=world.obstacles)

    def _safe_plan_path(self, start, destination):
        return self.path_planner.plan_path(start, destination)

    def move_drone(self, drone):
        # اگر به مقصد رسیده باشه کاری نکن
        if drone.position == drone.destination:
            return

        next_step = None
        if drone.path and len(drone.path) > 1:
            next_step = drone.path[1]
        else:
            drone.path = self._safe_plan_path(drone.position, drone.destination)
            if len(drone.path) > 1:
                next_step = drone.path[1]

        if next_step:
            if not self.world.check_collision(next_step):
                drone.position = next_step
                drone.path.pop(0)
            else:
                drone.collision_avoided += 1
                drone.path = self._safe_plan_path(drone.position, drone.destination)
