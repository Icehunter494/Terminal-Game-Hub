import curses
import random
import time

# ----------------------------
# WORD BANK
# ----------------------------
WORDS = {
    "easy": [
        "cat", "dog", "tree", "book", "fish", "milk", "sun", "game"
    ],
    "medium": [
        "planet", "rocket", "python", "castle", "bridge",
        "forest", "island", "battle", "shadow"
    ],
    "hard": [
        "algorithm", "quantum", "neural", "synthesis",
        "galaxy", "cryptic", "voltage", "entropy"
    ]
}

# ----------------------------
# SCRAMBLE FUNCTION
# ----------------------------
def scramble(word):
    word = list(word)
    random.shuffle(word)
    return "".join(word)

# ----------------------------
# MENU
# ----------------------------
def menu(stdscr):
    stdscr.keypad(True)
    stdscr.nodelay(False)

    options = ["Start", "Quit"]
    selected = 0

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        title = "WORD SCRAMBLE"
        stdscr.addstr(h//2 - 4, w//2 - len(title)//2, title)

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
                return difficulty_menu(stdscr)
            else:
                return None

# ----------------------------
# DIFFICULTY
# ----------------------------
def difficulty_menu(stdscr):
    stdscr.keypad(True)
    stdscr.nodelay(False)

    options = ["Easy", "Medium", "Hard"]
    selected = 0

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(h//2 - 3, w//2 - 5, "DIFFICULTY")

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
            return options[selected].lower()

# ----------------------------
# GAME
# ----------------------------
def play_game(stdscr, difficulty):
    stdscr.keypad(True)
    stdscr.nodelay(True)

    score = 0
    rounds = 5

    for _ in range(rounds):
        word = random.choice(WORDS[difficulty])
        scrambled = scramble(word)

        start_time = time.time()
        guess = ""

        while True:
            stdscr.erase()
            h, w = stdscr.getmaxyx()

            # UI
            stdscr.addstr(2, w//2 - 10, f"Scrambled: {scrambled}")
            stdscr.addstr(4, w//2 - 10, f"Guess: {guess}")
            stdscr.addstr(6, w//2 - 10, f"Score: {score}")
            stdscr.addstr(8, w//2 - 10, "Type letters | Enter = submit | Q = quit")

            # timer
            elapsed = int(time.time() - start_time)
            stdscr.addstr(10, w//2 - 10, f"Time: {elapsed}s")

            stdscr.refresh()

            key = stdscr.getch()

            if key == -1:
                continue

            # quit anytime
            if key == ord('q'):
                return score

            # enter submit
            if key in [10, 13]:
                if guess == word:
                    score += 1
                break

            # backspace
            if key in [8, 127]:
                guess = guess[:-1]

            # letters only
            elif 97 <= key <= 122:
                guess += chr(key)

    stdscr.erase()
    stdscr.addstr(10, 10, f"GAME OVER | Score: {score}")
    stdscr.refresh()
    time.sleep(2)

    return score

# ----------------------------
# MAIN LOOP
# ----------------------------
def run(stdscr):
    curses.curs_set(0)

    while True:
        difficulty = menu(stdscr)

        if difficulty is None:
            break

        play_game(stdscr, difficulty)

# ----------------------------
# ENTRY
# ----------------------------
def main():
    curses.wrapper(run)

if __name__ == "__main__":
    main()