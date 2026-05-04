import curses
import random
import time
import json
import os

SAVE_FILE = "snake_highscore.json"

# ----------------------------
# HIGH SCORE
# ----------------------------
def load_highscore():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f).get("highscore", 0)
    return 0

def save_highscore(score):
    with open(SAVE_FILE, "w") as f:
        json.dump({"highscore": score}, f)

# ----------------------------
# MENU
# ----------------------------
def menu(stdscr):
    options = ["Start", "Difficulty", "Quit"]
    selected = 0
    difficulty = 0.10  # movement speed

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(h//2 - 4, w//2 - 3, "SNAKE")

        for i, opt in enumerate(options):
            x = w//2 - len(opt)//2
            y = h//2 - 1 + i

            if i == selected:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, opt)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, opt)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
        elif key in [10, 13]:

            if options[selected] == "Start":
                return difficulty
            elif options[selected] == "Difficulty":
                difficulty = difficulty_menu(stdscr)
            else:
                return None

# ----------------------------
# DIFFICULTY MENU
# ----------------------------
def difficulty_menu(stdscr):
    options = ["Easy", "Normal", "Hard"]
    speeds = [0.15, 0.10, 0.06]
    selected = 1

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(h//2 - 3, w//2 - 8, "Difficulty")

        for i, opt in enumerate(options):
            x = w//2 - len(opt)//2
            y = h//2 - 1 + i

            if i == selected:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, opt)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, opt)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % 3
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % 3
        elif key in [10, 13]:
            return speeds[selected]

# ----------------------------
# GAME
# ----------------------------
def game(stdscr, move_interval):
    curses.curs_set(0)
    stdscr.nodelay(1)

    h, w = stdscr.getmaxyx()

    snake = [[h//2, w//2], [h//2, w//2 - 1], [h//2, w//2 - 2]]
    direction = curses.KEY_RIGHT

    food = [random.randint(1, h-2), random.randint(1, w-2)]

    score = 0
    high = load_highscore()

    last_move = time.time()

    while True:
        stdscr.erase()
        stdscr.border()

        # INPUT (instant direction change)
        key = stdscr.getch()
        if key == ord('q'):
            return score

        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            direction = key

        # TIME-BASED MOVEMENT FIX
        now = time.time()
        if now - last_move < move_interval:
            # still draw current frame without moving
            pass
        else:
            last_move = now

            head = snake[0].copy()

            if direction == curses.KEY_UP:
                head[0] -= 1
            elif direction == curses.KEY_DOWN:
                head[0] += 1
            elif direction == curses.KEY_LEFT:
                head[1] -= 1
            elif direction == curses.KEY_RIGHT:
                head[1] += 1

            # collision walls
            if head[0] <= 0 or head[0] >= h-1 or head[1] <= 0 or head[1] >= w-1:
                return score

            # collision self
            if head in snake:
                return score

            snake.insert(0, head)

            # eat food
            if head == food:
                score += 1
                food = [random.randint(1, h-2), random.randint(1, w-2)]
            else:
                tail = snake.pop()
                stdscr.addch(tail[0], tail[1], ' ')

        # DRAW FOOD
        stdscr.addch(food[0], food[1], '*')

        # DRAW SNAKE
        stdscr.addch(snake[0][0], snake[0][1], 'O')
        for s in snake[1:]:
            stdscr.addch(s[0], s[1], '#')

        # UI
        stdscr.addstr(0, 2, f"Score: {score}  High: {high}")

        stdscr.refresh()

# ----------------------------
# GAME OVER
# ----------------------------
def game_over(stdscr, score):
    high = load_highscore()
    if score > high:
        save_highscore(score)
        high = score

    options = ["Restart", "Menu", "Quit"]
    selected = 0

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(h//2 - 3, w//2 - 10, f"Game Over: {score}")
        stdscr.addstr(h//2 - 2, w//2 - 10, f"High Score: {high}")

        for i, opt in enumerate(options):
            x = w//2 - len(opt)//2
            y = h//2 + i

            if i == selected:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, opt)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, opt)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % 3
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % 3
        elif key in [10, 13]:
            return options[selected]

# ----------------------------
# MAIN LOOP
# ----------------------------
def run(stdscr):
    while True:
        speed = menu(stdscr)

        if speed is None:
            break

        while True:
            score = game(stdscr, speed)
            choice = game_over(stdscr, score)

            if choice == "Restart":
                continue
            elif choice == "Menu":
                break
            else:
                return

def main():
    curses.wrapper(run)

def run_game():
    curses.wrapper(run)

if __name__ == "__main__":
    main()