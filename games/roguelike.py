import curses, random, time
from games.map_gen import MapGenerator
from games.rogue_classes import Entity, Item

def battle_scene(stdscr, player, enemy):
    sh, sw = stdscr.getmaxyx()
    log = f"A wild {enemy.name} appeared!"
    while enemy.hp > 0 and player.hp > 0:
        stdscr.erase()
        stdscr.addstr(2, 5, f"{enemy.name.upper()} HP: {enemy.hp}/{enemy.max_hp}")
        stdscr.addstr(sh-10, sw-30, f"{player.name.upper()} HP: {player.hp}/{player.max_hp}")
        stdscr.addstr(sh-6, 5, f"> {log}")
        stdscr.addstr(sh-4, 5, "(1) Tackle (2) BASH (Skill) (3) Run")
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('1'):
            dmg = player.damage + random.randint(-2, 2)
            log = f"Tackle dealt {dmg} damage!"
            enemy.hp -= dmg
        elif key == ord('2'):
            dmg = player.damage + 12
            log = f"POWER BASH! Dealt {dmg} damage!"
            enemy.hp -= dmg
        elif key == ord('3'): return "fled"
        else: continue

        stdscr.refresh()
        time.sleep(1)
        if enemy.hp > 0:
            e_dmg = enemy.damage + random.randint(-1, 1)
            player.hp -= e_dmg
            log = f"{enemy.name} hit back for {e_dmg}!"
            stdscr.refresh()
            time.sleep(1)
    return "won" if player.hp > 0 else "lost"

def run():
    curses.wrapper(game_loop)

def game_loop(stdscr):
   curses.curs_set(0)
   sh, sw = stdscr.getmaxyx()
   gen = MapGenerator(sw -20, sh -5)
   game_map, rooms = gen.generate()
   visited = [[False for _ in range(sw)] for _ in range(sh)]

   px, py = rooms[0]
   player = Entity("Hero", px, py, '@', 100, 10)
   enemies = [Entity("Goblin", r[0], r[1], 'g', 30, 5) for r in rooms[1:]]
   items = [Item("Potion", r[0]+1, r[1], '!', 25) for r in rooms[1:]]

   while True:
       stdscr.erase()
       for y, row in enumerate(game_map):
           for x, char in enumerate(row):
               if ((x-player.x)**2 + (y-player.y)**2)**0.5 < 5: visited[y][x] = True
               if visited[y][x]: stdscr.addch(y, x, char)

       for en in enemies:
           if en.hp > 0 and visited[en.y][en.x]: stdscr.addch(en.y, en.x, en.char, curses.A_REVERSE)
       for itm in items:
           if visited[itm.y][itm.x]: stdscr.addch(itm.y, itm.x, itm.char, curses.A_BOLD)

       stdscr.addch(player.y, player.x, player.char, curses.A_BOLD)
       stdscr.addstr(1, sw-18, f"HP: {player.hp}/{player.max_hp}")
       
       key = stdscr.getch()
       nx, ny = player.x, player.y
       if key == curses.KEY_UP: ny -= 1
       elif key == curses.KEY_DOWN: ny += 1
       elif key == curses.KEY_LEFT: nx -= 1
       elif key == curses.KEY_RIGHT: nx += 1
       elif key == ord('q'): break

       target_en = next((e for e in enemies if e.x == nx and e.y == ny and e.hp > 0), None)
       if target_en:
           if battle_scene(stdscr, player, target_en) == "won": target_en.hp = 0
           elif player.hp <= 0: break
       elif game_map[ny][nx] == '.':
           player.x, player.y = nx, ny

       for itm in items[:]:
           if player.x == itm.x and player.y == itm.y:
               player.hp = min(player.max_hp, player.hp + itm.power)
               items.remove(itm)
       stdscr.refresh()