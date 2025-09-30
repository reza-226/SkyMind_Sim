import numpy as np
import heapq  # Import the heapq module for the priority queue

class PathPlanner:
    """
    Handles pathfinding for the drone using the A* algorithm on a 3D grid.
    """
    def __init__(self, environment):
        """
        Initializes the PathPlanner with the simulation environment.

        Args:
            environment (Environment): The environment object containing the grid and obstacles.
        """
        self.env = environment
        self.grid = self.env.grid
        print("PathPlanner initialized.")

    def _heuristic(self, a, b):
        """
        Calculate the Euclidean distance heuristic between two points.

        Args:
            a (tuple): The (x, y, z) coordinates of the first point.
            b (tuple): The (x, y, z) coordinates of the second point.

        Returns:
            float: The straight-line distance between the two points.
        """
        return np.linalg.norm(np.array(a) - np.array(b))

    def _get_neighbors(self, node):
        """
        Get the valid neighbors of a node on the grid.
        A neighbor is valid if it's within the grid bounds and not an obstacle.
        """
        neighbors = []
        # Define 26 possible directions in 3D space (including diagonals)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == 0 and dy == 0 and dz == 0:
                        continue  # Skip the node itself

                    nx, ny, nz = node[0] + dx, node[1] + dy, node[2] + dz

                    # Check if the neighbor is within bounds
                    if (0 <= nx < self.grid.shape[0] and
                        0 <= ny < self.grid.shape[1] and
                        0 <= nz < self.grid.shape[2]):
                        
                        # Check if the neighbor is not an obstacle
                        if self.grid[nx, ny, nz] == 0:
                            # Calculate the cost to move to this neighbor
                            # 1 for cardinal, sqrt(2) for 2D diagonal, sqrt(3) for 3D diagonal
                            cost = np.sqrt(dx**2 + dy**2 + dz**2)
                            neighbors.append(((nx, ny, nz), cost))
        return neighbors

    def find_path_a_star(self, start_pos, goal_pos):
        """
        Finds a path from a start to a goal position using the A* algorithm.

        Args:
            start_pos (tuple): The (x, y, z) starting coordinates.
            goal_pos (tuple): The (x, y, z) goal coordinates.

        Returns:
            list: A list of (x, y, z) tuples representing the path, or None if no path is found.
        """
        print(f"Starting A* search from grid {start_pos} to {goal_pos}...")

        start_node = tuple(np.floor(start_pos).astype(int))
        goal_node = tuple(np.floor(goal_pos).astype(int))

        # Check if start or goal are in an obstacle
        if self.grid[start_node]:
            print(f"A* search failed: Start node {start_node} is inside an obstacle.")
            return None
        if self.grid[goal_node]:
            print(f"A* search failed: Goal node {goal_node} is inside an obstacle.")
            return None

        # The set of nodes to be evaluated, implemented as a priority queue (min-heap)
        # Items are (f_score, node)
        open_set = [(0, start_node)]
        heapq.heapify(open_set)

        # Dictionary to reconstruct the path
        came_from = {}

        # g_score: Cost from start to the current node
        g_score = {start_node: 0}

        # f_score: Total estimated cost from start to goal through this node (g_score + heuristic)
        # We can calculate f_score on the fly, as the heap is sorted by it.

        iteration_count = 0
        
        while open_set:
            iteration_count += 1
            if iteration_count % 5000 == 0:
                print(f"A* iterations: {iteration_count} | Open set size: {len(open_set)}")

            # Get the node with the lowest f_score from the priority queue
            current_f_score, current_node = heapq.heappop(open_set)

            if current_node == goal_node:
                print(f"Path found! Reconstructing path from {len(came_from)} nodes...")
                return self._reconstruct_path(came_from, current_node)

            for neighbor, move_cost in self._get_neighbors(current_node):
                # tentative_g_score is the distance from start to the neighbor through current
                tentative_g_score = g_score[current_node] + move_cost

                # If this path to neighbor is better than any previous one, record it
                if neighbor not in g_score or tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self._heuristic(neighbor, goal_node)
                    
                    # Add the neighbor to the open set for evaluation
                    heapq.heappush(open_set, (f_score, neighbor))
        
        print(f"A* search failed after {iteration_count} iterations: No path found from start to goal.")
        return None

    def _reconstruct_path(self, came_from, current):
        """Reconstructs the path from the goal back to the start."""
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        path = total_path[::-1]  # Reverse the path to get start -> goal
        print(f"Path reconstructed with {len(path)} steps.")
        return path
