import curses
import random
import time

def run():

    curses.wrapper(game_loop)

def game_loop(stdscr):
    # Essential Settings
    curses.curs_set(0)     # Hide cursor
    stdscr.nodelay(True)   # Don't wait for input
    
    sh, sw = stdscr.getmaxyx()
    player_y, player_x = sh // 2, sw // 2
    bullets = []
    score = 0

    while True:
        # 1. INPUT FLUSH (Fixes the "too fast" movement)
        key = -1
        while True:
            k = stdscr.getch()
            if k == -1: break
            key = k

        if key == ord('q'): break
        if key == curses.KEY_UP and player_y > 1: player_y -= 1
        if key == curses.KEY_DOWN and player_y < sh - 2: player_y += 1
        if key == curses.KEY_LEFT and player_x > 1: player_x -= 1
        if key == curses.KEY_RIGHT and player_x < sw - 2: player_x += 1

        # 2. GAME LOGIC
        # Lowered spawn rate to 0.08 so it's not impossible
        if random.random() < 0.08:
            bullets.append([1, random.randint(1, sw - 2)])
        
        new_bullets = []
        collision = False
        for b_y, b_x in bullets:
            b_y += 1 # Move bullet down
            if b_y == player_y and b_x == player_x:
                collision = True
            if b_y < sh - 1:
                new_bullets.append([b_y, b_x])
        bullets = new_bullets
        score += 1

        # 3. RENDER (Draw everything at once)
        stdscr.erase()
        
        try:
            stdscr.addstr(0, 0, f"SCORE: {score} | Arrows to move | 'q' to Quit")
            for b_y, b_x in bullets:
                stdscr.addch(b_y, b_x, '*')
            stdscr.addch(player_y, player_x, 'A', curses.A_BOLD)
            stdscr.refresh()
        except curses.error:
            pass # Prevents crash if terminal is too small

        if collision:
            stdscr.addstr(sh//2, sw//2 - 5, " GAME OVER! ")
            stdscr.refresh()
            time.sleep(1.5)
            break

        # 4. SPEED CONTROL
        # 80ms is roughly 12 frames per second. 
        # Increase this number to slow the game down more.
        curses.napms(80) 

