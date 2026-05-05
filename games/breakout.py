import curses
import time
import random

PADDLE_WIDTH = 9
FRAME_DELAY = 0.04

BRICK_ROWS = 6
BRICK_COLS = 12

def create_bricks():
    return [[1 for _ in range(BRICK_COLS)] for _ in range(BRICK_ROWS)]

def draw_bricks(stdscr, bricks):
    for y, row in enumerate(bricks):
        for x, val in enumerate(row):
            if val:
                stdscr.addstr(2 + y, 2 + x * 2, "[]")

def clamp(v, mi, ma):
    return max(mi, min(v, ma))

def run(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(True)

    h, w = stdscr.getmaxyx()

    while True:
        paddle_x = w // 2

        # SAFE BALL START (above paddle)
        ball_x = w // 2
        ball_y = h - 5

        ball_dx = random.choice([-1, 1])
        ball_dy = -1

        bricks = create_bricks()
        score = 0

        while True:
            stdscr.erase()

            key = stdscr.getch()

            if key == ord('q'):
                return
            if key == ord('r'):
                break

            if key == curses.KEY_LEFT:
                paddle_x -= 2
            elif key == curses.KEY_RIGHT:
                paddle_x += 2

            paddle_x = clamp(paddle_x, 1, w - PADDLE_WIDTH - 1)

            # MOVE BALL
            ball_x += ball_dx
            ball_y += ball_dy

            # WALL BOUNCE
            if ball_x <= 1 or ball_x >= w - 2:
                ball_dx *= -1

            if ball_y <= 1:
                ball_dy *= -1

            # ----------------------------
            # PADDLE COLLISION (FIXED)
            # ----------------------------
            paddle_y = h - 2

            if ball_y == paddle_y - 1:
                if paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH:
                    ball_dy = -1

                    # angle control (based on where it hits paddle)
                    offset = ball_x - (paddle_x + PADDLE_WIDTH // 2)
                    ball_dx = max(-2, min(2, offset // 2))

            # ----------------------------
            # BRICK COLLISION
            # ----------------------------
            bx = (ball_x - 2) // 2
            by = ball_y - 2

            if 0 <= by < BRICK_ROWS and 0 <= bx < BRICK_COLS:
                if bricks[by][bx]:
                    bricks[by][bx] = 0
                    ball_dy *= -1
                    score += 10

            # ----------------------------
            # GAME OVER (FIXED)
            # ----------------------------
            if ball_y >= h - 1:
                stdscr.addstr(h // 2, w // 2 - 5, "GAME OVER")
                stdscr.addstr(h // 2 + 1, w // 2 - 12, "R = Restart | Q = Quit")
                stdscr.refresh()

                while True:
                    k = stdscr.getch()
                    if k == ord('q'):
                        return
                    if k == ord('r'):
                        break
                break

            # ----------------------------
            # WIN
            # ----------------------------
            if all(all(cell == 0 for cell in row) for row in bricks):
                stdscr.addstr(h // 2, w // 2 - 4, "YOU WIN!")
                stdscr.refresh()
                time.sleep(2)
                break

            # DRAW
            stdscr.addstr(0, 2, f"Score: {score} | Q Quit | R Restart")

            draw_bricks(stdscr, bricks)

            stdscr.addstr(paddle_y, paddle_x, "=" * PADDLE_WIDTH)
            stdscr.addstr(ball_y, ball_x, "O")

            stdscr.refresh()
            time.sleep(FRAME_DELAY)