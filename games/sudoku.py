import curses
import random
import copy
import time

# ----------------------------
# VALIDATION
# ----------------------------
def is_valid(board, r, c, n):
    for i in range(9):
        if board[r][i] == n or board[i][c] == n:
            return False

    sr, sc = (r // 3) * 3, (c // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[sr + i][sc + j] == n:
                return False

    return True

# ----------------------------
# BOARD GENERATION
# ----------------------------
def fill_board(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)

                for n in nums:
                    if is_valid(board, r, c, n):
                        board[r][c] = n
                        if fill_board(board):
                            return True
                        board[r][c] = 0
                return False
    return True


def remove_cells(board, difficulty):
    count = difficulty
    while count > 0:
        r = random.randint(0, 8)
        c = random.randint(0, 8)

        if board[r][c] != 0:
            board[r][c] = 0
            count -= 1


def generate_puzzle(difficulty):
    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_board(board)

    solution = copy.deepcopy(board)
    remove_cells(board, difficulty)

    return board, solution

# ----------------------------
# MENU
# ----------------------------
def menu(stdscr):
    stdscr.keypad(True)
    stdscr.timeout(100)

    options = ["Play", "Quit"]
    selected = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        title = "SUDOKU"
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

        if key == -1:
            continue

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
        elif key in [10, 13]:

            if options[selected] == "Play":
                diff = difficulty_menu(stdscr)

                while True:
                    win = play_game(stdscr, diff)
                    if not win:
                        break
                return
            else:
                return

# ----------------------------
# DIFFICULTY MENU (FIXED NO FREEZE)
# ----------------------------
def difficulty_menu(stdscr):
    stdscr.keypad(True)
    stdscr.timeout(100)

    options = ["Easy", "Medium", "Hard"]
    values = [30, 45, 55]
    selected = 0

    while True:
        stdscr.clear()
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

        if key == -1:
            continue

        if key == curses.KEY_UP:
            selected = (selected - 1) % 3
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % 3
        elif key in [10, 13]:
            return values[selected]

# ----------------------------
# GAME
# ----------------------------
def play_game(stdscr, difficulty):
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.timeout(100)

    board, solution = generate_puzzle(difficulty)
    original = copy.deepcopy(board)

    cursor = [0, 0]

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        start_y = h//2 - 6
        start_x = w//2 - 12

        # DRAW BOARD
        for r in range(9):
            for c in range(9):
                val = board[r][c]
                x = start_x + c * 2
                y = start_y + r

                if (r, c) == tuple(cursor):
                    stdscr.attron(curses.A_REVERSE)

                if val == 0:
                    stdscr.addstr(y, x, ". ")
                else:
                    stdscr.addstr(y, x, str(val) + " ")

                if (r, c) == tuple(cursor):
                    stdscr.attroff(curses.A_REVERSE)

        stdscr.addstr(start_y + 11, start_x, "Arrows: move | 1-9: input | Q: quit")

        stdscr.refresh()

        key = stdscr.getch()

        if key == -1:
            continue

        # movement
        if key == curses.KEY_UP:
            cursor[0] = max(0, cursor[0] - 1)
        elif key == curses.KEY_DOWN:
            cursor[0] = min(8, cursor[0] + 1)
        elif key == curses.KEY_LEFT:
            cursor[1] = max(0, cursor[1] - 1)
        elif key == curses.KEY_RIGHT:
            cursor[1] = min(8, cursor[1] + 1)

        elif key == ord('q'):
            return False

        # input number
        elif ord('1') <= key <= ord('9'):
            r, c = cursor

            if original[r][c] == 0:
                board[r][c] = key - ord('0')

        # win check
        if board == solution:
            stdscr.clear()
            stdscr.addstr(10, 10, "YOU SOLVED IT!")
            stdscr.refresh()
            time.sleep(2)
            return True

# ----------------------------
# RUNNER
# ----------------------------
def run(stdscr):
    curses.curs_set(0)
    menu(stdscr)

def main():
    curses.wrapper(run)

if __name__ == "__main__":
    main()