# File: D:\Payannameh\SkyMind_Sim\skymind_sim\layer_0_presentation\environment.py
# -*- coding: utf-8 -*-
import json
import os
import logging
import numpy as np
import random
from skymind_sim.layer_3_intelligence.pathfinding.a_star import safe_a_star_search

class Environment:
    def __init__(self, window_config, grid_config, simulation_config):
        self.window_config = window_config
        self.grid_config = grid_config
        self.simulation_config = simulation_config

        self.paths = []
        self.obstacles = []
        self.test_drone_pos = None
        self.test_drone_speed = simulation_config.get("test_drone_speed", 1.0)
        self.test_drone_path = []
        self.path_index = 0
        self.move_accumulator = 0.0
        self.last_goal = None  # ذخیره آخرین مقصد

        map_path = simulation_config.get("map_path")
        if not map_path:
            raise ValueError("Missing 'map_path' in simulation_config")

        self.map_data = self.load_map(map_path)
        self._extract_obstacles()
        logging.info(f"Environment initialized with map: {map_path}")

    def load_map(self, map_path):
        if not os.path.exists(map_path):
            raise FileNotFoundError(f"Map file not found: {map_path}")
        if map_path.endswith(".txt"):
            with open(map_path, "r", encoding="utf-8") as f:
                return [list(line.rstrip("\n")) for line in f]
        elif map_path.endswith(".json"):
            with open(map_path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            raise ValueError(f"Unsupported map format: {map_path}")

    def _extract_obstacles(self):
        obstacles = []
        if isinstance(self.map_data, list):
            for y, row in enumerate(self.map_data):
                for x, cell in enumerate(row):
                    if cell == "#":
                        obstacles.append((x, y))
        elif isinstance(self.map_data, dict):
            obstacles.extend(self.map_data.get("obstacles", []))
        self.obstacles = obstacles
        logging.info(f"Extracted {len(self.obstacles)} obstacles from map.")

    def _build_grid_array(self):
        rows = len(self.map_data)
        cols = len(self.map_data[0])
        grid = np.zeros((rows, cols), dtype=int)
        for x, y in self.obstacles:
            grid[y, x] = 1
        return grid

    def get_obstacles_data(self):
        cell_size = self.grid_config.get("cell_size", 32)
        return [
            (x * cell_size, y * cell_size, cell_size, cell_size)
            for (x, y) in self.obstacles
        ]

    def set_paths(self, paths):
        if isinstance(paths, list):
            self.paths = paths

    def get_path_to_draw(self):
        cell_size = self.grid_config.get("cell_size", 32)
        return [
            [(x * cell_size, y * cell_size) for (x, y) in path]
            for path in self.paths
        ]

    def _find_free_goal(self):
        """انتخاب هوشمند مقصد آزاد و مسیرپذیر."""
        rows = len(self.map_data)
        cols = len(self.map_data[0])
        free_cells = [
            (x, y)
            for y in range(rows)
            for x in range(cols)
            if (x, y) not in self.obstacles and (x, y) != self.test_drone_pos
        ]

        # حذف آخرین مقصد از انتخاب
        if self.last_goal:
            free_cells = [cell for cell in free_cells if cell != self.last_goal]

        # مرتب‌سازی: دورترین مقصدها اول
        free_cells.sort(
            key=lambda c: abs(c[0] - self.test_drone_pos[0]) + abs(c[1] - self.test_drone_pos[1]),
            reverse=True
        )

        grid_array = self._build_grid_array()
        for goal in free_cells:
            path = safe_a_star_search(grid_array, self.test_drone_pos, goal)
            if path and path != [self.test_drone_pos]:
                self.last_goal = goal
                return goal
        return None

    def _generate_path(self, start):
        """تولید مسیر با fallback و سرعت پویا."""
        goal = self._find_free_goal()
        grid_array = self._build_grid_array()

        if goal is None:
            logging.warning("No reachable goal found in map — using nearest free cell.")
            path = safe_a_star_search(grid_array, start, start)
        else:
            path = safe_a_star_search(grid_array, start, goal)

        if not path:
            path = [start]

        # تنظیم سرعت براساس طول مسیر
        self._adjust_speed(len(path))

        # لاگ گرافیکی مسیر
        self._log_path_map(path)

        logging.info(f"A* path generated: {start} → {path[-1]} ({len(path)} steps)")
        return path[1:] if len(path) > 1 else [start]

    def _adjust_speed(self, path_length):
        base_speed = self.simulation_config.get("test_drone_speed", 1.0)
        if path_length > 20:
            self.test_drone_speed = base_speed * 1.5
        elif path_length < 10:
            self.test_drone_speed = base_speed * 0.8
        else:
            self.test_drone_speed = base_speed
        logging.info(f"Drone speed adjusted to {self.test_drone_speed:.2f}")

    def _log_path_map(self, path):
        rows = len(self.map_data)
        cols = len(self.map_data[0])
        grid_visual = [["." for _ in range(cols)] for _ in range(rows)]
        for ox, oy in self.obstacles:
            grid_visual[oy][ox] = "#"
        for px, py in path:
            grid_visual[py][px] = "*"
        sx, sy = path[0]
        gx, gy = path[-1]
        grid_visual[sy][sx] = "S"
        grid_visual[gy][gx] = "G"
        logging.info("\n" + "\n".join("".join(row) for row in grid_visual))

    def update(self, dt):
        if self.test_drone_pos is None:
            self.test_drone_pos = (0, 0)
            self.test_drone_path = self._generate_path(self.test_drone_pos)
            self.paths = [[self.test_drone_pos]]
            self.path_index = 0
            self.move_accumulator = 0.0
            return

        if self.path_index >= len(self.test_drone_path):
            logging.info("Test drone reached goal, regenerating path.")
            self.test_drone_path = self._generate_path(self.test_drone_pos)
            self.paths = [[self.test_drone_pos]]
            self.path_index = 0
            self.move_accumulator = 0.0
            return

        self.move_accumulator += dt
        step_time = 1.0 / self.test_drone_speed
        if self.move_accumulator >= step_time:
            self.move_accumulator -= step_time
            next_pos = self.test_drone_path[self.path_index]
            self.test_drone_pos = next_pos
            self.paths[0].append(next_pos)
            self.path_index += 1
