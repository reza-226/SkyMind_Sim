# skymind_sim/pathfinding/path_planner.py

import heapq

class PathPlanner:
    """
    Plans a path from a start to an end point using the A* algorithm.
    """
    def __init__(self, environment):
        """
        Initializes the path planner with the simulation environment.

        Args:
            environment (Environment): The environment containing obstacles and dimensions.
        """
        self.env = environment
        self.width, self.depth, self.height = self.env.get_dimensions()

    def _heuristic(self, a, b):
        """
        Calculates the Manhattan distance heuristic between two points.
        This is a common and efficient heuristic for grid-based pathfinding.
        """
        (x1, y1, z1) = a
        (x2, y2, z2) = b
        return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

    def _get_neighbors(self, node):
        """
        Gets the valid neighbors of a given node (point in 3D space).
        A neighbor is valid if it is within the environment bounds and not an obstacle.
        """
        x, y, z = node
        neighbors = []
        # We consider 6 directions: up, down, left, right, forward, backward
        for dx, dy, dz in [(0,0,1), (0,0,-1), (0,1,0), (0,-1,0), (1,0,0), (-1,0,0)]:
            nx, ny, nz = x + dx, y + dy, z + dz

            # Check if the neighbor is within bounds
            if not (0 <= nx < self.width and 0 <= ny < self.depth and 0 <= nz < self.height):
                continue
            
            # Check if the neighbor is an obstacle
            if self.env.is_obstacle(nx, ny, nz):
                continue
                
            neighbors.append((nx, ny, nz))
        return neighbors

    def _reconstruct_path(self, came_from, current):
        """
        Reconstructs the path from the end node back to the start node.
        """
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1] # Reverse the path to get start -> end

    def plan_path(self, start, end):
        """
        Finds the shortest path from start to end using A*.

        Args:
            start (tuple): The (x, y, z) starting coordinate.
            end (tuple): The (x, y, z) ending coordinate.

        Returns:
            list: A list of (x, y, z) tuples representing the path, or None if no path is found.
        """
        open_set = []
        heapq.heappush(open_set, (0, start)) # (priority, node)

        came_from = {}
        
        g_score = {start: 0} # Cost from start to the current node
        
        f_score = {start: self._heuristic(start, end)} # Estimated cost from start to end through this node

        open_set_hash = {start}

        while open_set:
            # Get the node in open_set with the lowest f_score
            current = heapq.heappop(open_set)[1]
            open_set_hash.remove(current)

            if current == end:
                return self._reconstruct_path(came_from, current)

            for neighbor in self._get_neighbors(current):
                # The distance from start to a neighbor is the distance from start to current + 1
                tentative_g_score = g_score.get(current, float('inf')) + 1

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    # This path to neighbor is better than any previous one. Record it!
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self._heuristic(neighbor, end)
                    
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)
        
        # Open set is empty but goal was never reached
        return None
