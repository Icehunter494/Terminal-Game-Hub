import curses
import random
import time

# ----------------------------
# AI WORD GENERATOR
# ----------------------------
SYLLABLES = [
    "ar", "an", "el", "or", "in", "ex", "tar", "mor", "zen", "ul",
    "ka", "ra", "lo", "vi", "ne", "tri", "sol", "dex", "phi", "qua",
    "cy", "dr", "bl", "st", "gr", "pl", "th", "ion", "or", "en", "al"
]

ENDINGS = ["ion", "ity", "ous", "ive", "al", "er", "en", "ic", "or", "on"]

def generate_ai_word(difficulty):
    if difficulty == "easy":
        length = random.randint(2, 3)
    elif difficulty == "medium":
        length = random.randint(3, 4)
    else:
        length = random.randint(4, 6)

    word = ""

    for _ in range(length):
        word += random.choice(SYLLABLES)

    if difficulty != "easy" and random.random() < 0.6:
        word += random.choice(ENDINGS)

    return word.lower()

# ----------------------------
# HANGMAN STAGES
# ----------------------------
HANGMAN = [
    "",
    "O",
    "O\n|",
    "O\n/|",
    "O\n/|\\",
    "O\n/|\\\n/",
    "O\n/|\\\n/ \\"
]

# ----------------------------
# MAIN MENU
# ----------------------------
def menu(stdscr):
    stdscr.keypad(True)
    stdscr.nodelay(False)  # IMPORTANT: BLOCKING INPUT (prevents freeze bugs)

    options = ["Start", "Quit"]
    selected = 0

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        title = "AI HANGMAN"
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
# DIFFICULTY MENU (FIXED NO FREEZE)
# ----------------------------
def difficulty_menu(stdscr):
    stdscr.keypad(True)
    stdscr.nodelay(False)  # CRITICAL FIX

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
            stdscr.nodelay(True)  # switch back to game mode
            return options[selected].lower()

# ----------------------------
# GAME
# ----------------------------
def play_game(stdscr, difficulty):
    stdscr.keypad(True)
    stdscr.nodelay(True)  # non-blocking for gameplay

    word = generate_ai_word(difficulty)
    guessed = set()
    wrong = 0
    max_wrong = len(HANGMAN) - 1

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        # word display
        display = " ".join([c if c in guessed else "_" for c in word])
        stdscr.addstr(2, w//2 - len(display)//2, display)

        # hangman
        hang = HANGMAN[wrong].split("\n")
        for i, line in enumerate(hang):
            stdscr.addstr(5 + i, w//2 - 10, line)

        stdscr.addstr(13, w//2 - 10, f"Guessed: {' '.join(sorted(guessed))}")
        stdscr.addstr(15, w//2 - 10, "Type letters | Q to quit")

        stdscr.refresh()

        key = stdscr.getch()

        if key == -1:
            continue

        if key == ord('q'):
            return False

        if 97 <= key <= 122:
            letter = chr(key)

            if letter not in guessed:
                guessed.add(letter)

                if letter not in word:
                    wrong += 1

        # win
        if all(c in guessed for c in word):
            stdscr.clear()
            stdscr.addstr(h//2, w//2 - 5, "YOU WIN!")
            stdscr.refresh()
            time.sleep(2)
            return True

        # lose
        if wrong >= max_wrong:
            stdscr.clear()
            stdscr.addstr(h//2 - 1, w//2 - 7, "GAME OVER")
            stdscr.addstr(h//2, w//2 - len(word)//2, f"Word: {word}")
            stdscr.refresh()
            time.sleep(2)
            return False

# ----------------------------
# MAIN LOOP
# ----------------------------
def run(stdscr):
    curses.curs_set(0)

    while True:
        difficulty = menu(stdscr)

        if difficulty is None:
            break

        while True:
            result = play_game(stdscr, difficulty)
            if not result:
                break

def main():
    curses.wrapper(run)

if __name__ == "__main__":
    main()