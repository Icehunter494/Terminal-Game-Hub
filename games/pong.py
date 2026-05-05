import curses
import time

#settings
PADDLE_HEIGHT = 4
WIN_SCORE = 4
FRAME_DELAY = 0.05 #speed control


#helper
def draw_paddle(stdscr, x, y):
    for i in range(PADDLE_HEIGHT):
        stdscr.addstr(y + i, x, "!")

def clamp(val, min_v, max_v):
    return max(min_v, min(val, max_v))

# maingame
def run(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(True)

    h, w = stdscr.getmaxyx()

    #paddle pos
    left_y = h//2
    right_y = h//2

    #ball
    ball_x = w // 2
    ball_y = h // 2
    ball_dx = 1
    ball_dy = 1

    score_left = 0
    score_right = 0

    while True:
        stdscr.erase()

    #input
        key = stdscr.getch()

        #lft paddle(w/s)
        if key == ord('w'):
            left_y -= 1
        elif key == ord('s'):
            left_y += 1
        #right paddle
        elif key == curses.KEY_UP:
            right_y -= 1
        elif key == curses.KEY_DOWN:
            right_y += 1
        
        # Quit
        elif key == ord('q'):
            break

        #clamp pad

        left_y = clamp(left_y, 1, h - PADDLE_HEIGHT - 1)
        right_y = clamp(right_y, 1, h - PADDLE_HEIGHT - 1)

        #ball movement

        ball_x += ball_dx
        ball_y += ball_dy

        #top/bottom collision
        if ball_y <= 1 or ball_y >= h -2:
            ball_dy *= -1
        #left pad collision
        if ball_x == 3:
            if left_y <= ball_y <= left_y + PADDLE_HEIGHT:
                ball_dx *= -1
        #right pad collision
        if ball_x == w -4:
            if right_y <= ball_y <= right_y + PADDLE_HEIGHT:
                ball_dx *= -1
        
        #scoring
        if ball_x <= 0:
            score_right += 1
            ball_x, ball_y = w // 2, h // 2

        if ball_x >= w -1:
            score_left += 1
            ball_x, ball_y = w // 2, h // 2
        # win condish
        if score_left == WIN_SCORE or score_right == WIN_SCORE:
            stdscr.erase()
            winner = "LEFT PLAYER" if score_left == WIN_SCORE else "RIGHT PLAYER"
            stdscr.addstr(h // 2, w // 2 - 10, f"{winner} WINS!")
            stdscr.refresh()
            time.sleep(2)
            break

        #draw field
        stdscr.addstr(0, w // 2 - 5, f"{score_left} | {score_right}")

        #paddles
        draw_paddle(stdscr, 2, left_y)
        draw_paddle(stdscr, w - 3, right_y)

        #ball
        stdscr.addstr(ball_y, ball_x, "O")

        stdscr.refresh()
        time.sleep(FRAME_DELAY)