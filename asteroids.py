import curses
import time
import math
import random

FRAME_DELAY = 0.04

#ent clas
class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.vel_x = 0
        self.vel_y = 0

class Bullet:
    def __init__(self, x, y, angle):
        speed = 2
        self.x = x
        self.y = y
        self.vel_x = math.cos(angle) * speed
        self.vel_y = math.sin(angle) * speed
        self.life = 40

class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-0.7, 0.7)
        self.vel_y = random.uniform(-0.7, 0.7)

#wrap scrn
def wrap(obj, w, h):
    obj.x %= w
    obj.y %= h

#dis
def dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

#main game
def run(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    h, w = stdscr.getmaxyx()

    while True:
        #init
        ship = Ship(w // 2, h // 2)
        bullets = []
        asteroids = [Asteroid(random.randint(0, w), random.randint(0, h)) for _ in range(5)]
        score = 0

        while True:
            stdscr.erase()
            key = stdscr.getch()

            #input
            if key == ord('q'):
                return
            
            if key == curses.KEY_LEFT:
                ship.angle -= 0.2
            elif key == curses.KEY_RIGHT:
                ship.angle += 0.2
            elif key == curses.KEY_UP:
                ship.vel_x += math.cos(ship.angle) * 0.3
                ship.vel_y += math.sin(ship.angle) * 0.3
            elif key == ord(' '):
                bullets.append(Bullet(ship.x, ship.y, ship.angle))
            
            #update ship
            ship.x += ship.vel_x
            ship.y += ship.vel_y

            #fric
            ship.vel_x *= 0.99
            ship.vel_y *= 0.99

            wrap(ship, w, h)

            #up bull
            for b in bullets[:]:
                b.x += b.vel_x
                b.y += b.vel_y
                b.life -= 1

                wrap(b, w, h)

                if b.life <= 0:
                    bullets.remove(b)
            
            #up ast
            for a in asteroids:
                a.x += a.vel_x
                a.y += a.vel_y
                wrap(a, w, h)
            
            #collsions
            for a in asteroids[:]:
                #bull ht ast
                for b in bullets[:]:
                    if dist(a, b) < 1.5:
                        if b in bullets:
                            bullets.remove(b)
                        if a in asteroids:
                            asteroids.remove(a)
                        score += 10
                        asteroids.append(Asteroid(random.randint(0, w), random.randint(0, h)))
                        break
                
                #ast ht ship
                if dist(a, ship) < 1.5:
                    stdscr.erase()
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
            else:

                pass

            #draw

            stdscr.addstr(0, 2, f"Score: {score} | Q Quit")
            #ship tri
            sx = int(ship.x)
            sy = int(ship.y)
            stdscr.addstr(sy, sx, "A")

            #bull
            for b in bullets:
                stdscr.addstr(int(b.y), int(b.x), ".")
            #ast
            for a in asteroids:
                stdscr.addstr(int(a.y), int(a.x), "O")
            
            stdscr.refresh()
            time.sleep(FRAME_DELAY)