# -*- coding: utf-8 -*-
import heapq
import logging
import random

# --- استاندارد A* ---
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(current, rows, cols):
            if grid[neighbor[1]][neighbor[0]] == 1:  # obstacle
                continue

            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def get_neighbors(cell, rows, cols):
    x, y = cell
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < cols and 0 <= ny < rows:
            yield (nx, ny)

# --- تابع پیدا کردن نزدیک‌ترین خانه آزاد ---
def _find_nearest_free(grid, start):
    rows, cols = len(grid), len(grid[0])
    visited = set([start])
    queue = [start]

    while queue:
        cx, cy = queue.pop(0)
        if grid[cy][cx] == 0 and (cx, cy) != start:
            return (cx, cy)
        for nx, ny in get_neighbors((cx, cy), rows, cols):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
    return start  # اگر پیدا نکرد برمی‌گردیم به نقطه شروع

# --- نسخه ایمن A* با fallback ---
def safe_a_star_search(grid, start, goal):
    try:
        path = a_star_search(grid, start, goal)
        if path:
            return path
    except Exception as e:
        logging.warning(f"A* search failed: {e}")

    # مرحله دوم: مقصد نزدیک‌تر پیدا کن
    nearest_goal = _find_nearest_free(grid, start)
    if nearest_goal != start:
        logging.warning(f"No reachable goal found — rerouting to nearest free cell {nearest_goal}")
        alt_path = a_star_search(grid, start, nearest_goal)
        if alt_path:
            return alt_path

    # مرحله سوم: حرکت به اولین سلول آزاد اطراف
    for nx, ny in [(start[0]+1,start[1]), (start[0]-1,start[1]),
                   (start[0],start[1]+1), (start[0],start[1]-1)]:
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] == 0:
            logging.warning(f"No distant free cells — moving to adjacent free cell {(nx, ny)}")
            return [start, (nx, ny)]

    # مرحله چهارم: حرکت تصادفی به اطراف حتی اگر مانع باشه (برای جلوگیری از توقف)
    logging.warning("Map fully blocked — performing random fallback move.")
    rnd_moves = [(start[0]+dx, start[1]+dy) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]]
    rnd_moves = [(x,y) for x,y in rnd_moves if 0 <= y < len(grid) and 0 <= x < len(grid[0])]
    if rnd_moves:
        return [start, random.choice(rnd_moves)]

    # مرحله آخر: مجبوراً خود نقطه شروع (باید کم پیش بیاد)
    return [start]
