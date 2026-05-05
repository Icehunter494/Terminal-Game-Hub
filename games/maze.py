import curses
import random
import time
from collections import deque

# ----------------------------
# MAZE GENERATION
# ----------------------------
def generate_maze(w, h):
    maze = [[1 for _ in range(w)] for _ in range(h)]

    def carve(x, y):
        maze[y][x] = 0

        dirs = [(2,0), (-2,0), (0,2), (0,-2)]
        random.shuffle(dirs)

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy

            if 0 < nx < w-1 and 0 < ny < h-1:
                if maze[ny][nx] == 1:
                    maze[y + dy//2][x + dx//2] = 0
                    carve(nx, ny)

    carve(1, 1)

    start = (1, 1)
    end = (w - 2, h - 2)

    maze[start[1]][start[0]] = 0
    maze[end[1]][end[0]] = 0

    return maze, start, end

# ----------------------------
# SOLVER (BFS)
# ----------------------------
def solve_maze(maze, start, end):
    h, w = len(maze), len(maze[0])

    q = deque([start])
    visited = set([start])
    parent = {}

    while q:
        x, y = q.popleft()

        if (x, y) == end:
            break

        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < w and 0 <= ny < h:
                if maze[ny][nx] == 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    q.append((nx, ny))

    path = []
    cur = end

    while cur in parent:
        path.append(cur)
        cur = parent[cur]

    path.reverse()
    return path

# ----------------------------
# DRAW
# ----------------------------
def draw(stdscr, maze, player, end, level, path=None):
    stdscr.erase()

    for y in range(len(maze)):
        for x in range(len(maze[0])):

            char = " "

            if maze[y][x] == 1:
                char = "#"
            elif (x, y) == player:
                char = "P"
            elif (x, y) == end:
                char = "E"
            elif path and (x, y) in path:
                char = "."

            try:
                stdscr.addch(y, x, char)
            except:
                pass

    stdscr.addstr(0, 2, f"Level {level} | Arrows move | S solve | R restart | Q quit")
    stdscr.refresh()

# ----------------------------
# LEVEL GAME
# ----------------------------
def play_level(stdscr, level):
    curses.curs_set(0)

    # CRITICAL FIX: INPUT MODE
    stdscr.keypad(True)
    stdscr.nodelay(True)

    w = min(20 + level * 4, 80)
    h = min(10 + level * 2, 40)

    if w % 2 == 0: w += 1
    if h % 2 == 0: h += 1

    maze, start, end = generate_maze(w, h)
    player = list(start)

    solved_path = None
    show_solution = False

    while True:
        draw(stdscr, maze, tuple(player), end, level, solved_path if show_solution else None)

        key = stdscr.getch()

        if key == -1:
            continue

        # QUIT ANYTIME
        if key == ord('q'):
            return "quit"

        # RESTART LEVEL
        if key == ord('r'):
            return "restart"

        # SOLVE PATH
        if key == ord('s'):
            solved_path = solve_maze(maze, tuple(player), end)
            show_solution = True

        # MOVEMENT (FIXED RELIABLE ARROWS)
        nx, ny = player[0], player[1]

        if key == curses.KEY_UP:
            ny -= 1
        elif key == curses.KEY_DOWN:
            ny += 1
        elif key == curses.KEY_LEFT:
            nx -= 1
        elif key == curses.KEY_RIGHT:
            nx += 1
        else:
            continue

        if 0 <= nx < w and 0 <= ny < h:
            if maze[ny][nx] == 0:
                player = [nx, ny]

        # WIN CONDITION
        if tuple(player) == end:
            stdscr.clear()
            stdscr.addstr(10, 10, f"LEVEL {level} COMPLETE!")
            stdscr.refresh()
            time.sleep(1.5)
            return "win"

# ----------------------------
# MAIN LOOP (GLOBAL FIX APPLIED HERE)
# ----------------------------
def run(stdscr):
    curses.curs_set(0)

    # CRITICAL FIX FOR ARROWS
    stdscr.keypad(True)
    stdscr.nodelay(True)
    curses.use_default_colors()

    level = 1

    while True:
        result = play_level(stdscr, level)

        if result == "quit":
            break
        elif result == "restart":
            continue
        elif result == "win":
            level += 1

# ----------------------------
# ENTRY POINT
# ----------------------------
def main():
    curses.wrapper(run)

if __name__ == "__main__":
    main()