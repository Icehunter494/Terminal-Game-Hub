import random
import os

def create_board(size, mines):
    #crea board
    board = [[0 for _ in range(size)] for _ in range(size)]
    mine_locations  = set()

    #plant the boombooms
    while len(mine_locations) < mines:
        r, c = random.randint(0, size-1), random.randit(0, size-1)
        if (r, c) not in mine_locations:
            board[r][c] = '*'
            mine_locations.add((r, c))

    # Calc num for non-boom tiles
    for r in range(size):
        for c in range(size):
            if board[r][c] == '*': continue
            #see neighbors
            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < size and 0 <= nc < size and board[nr][nc] == '*':
                        count += 1
            board[r][c] = count
    return board
def reveal(r, c, board, visible, size):
    """Recursive function to pen up the map"""
    if not (0 <= r < size and 0 <= c < size) or visible[r][c]:
        return
    
    visible[r][c] = True

    #if 0 keep spread
    if board[r][c] == 0:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                reveal(r + dr, c + dc, board, visible, size)

def draw_board(board, visible, size):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(" " + " ".join(str(i) for i in range(size)))
    for r in range(size):
        row_str = [str(board[r][c]) if visible[r][c] else "#" for c in range(size)]
        print(f"{chr(65+r)} | " + " ".join(row_str))

def run():
    size = 10
    num_mines = 12
    board = create_board(size, num_mines)
    visible = [[False for _ in range(size)] for _ in range(size)]

    while True:
        draw_board(board, visible, size)
        cmd = input("\nEnter Target (e.g., A5) or 'Q': ").upper().strip()

        if cmd == 'Q': break
        if len(cmd) < 2 or not cmd[0].isalpha(): continue

        r, c = ord(cmd[0]) - 65, int(cmd[1:])

        if not (0 <= r < size and 0 <= c < size):
            print("Out of bounds!")
            continue

        if board[r][c] == '*':
            for r_idx in range(size):
                for c_idx in range(size):
                    if board[r_idx][c_idx] == '*': visible[r_idx][c_idx] = True
            draw_board(board, visible, size)
            print("\nBOOM! Game Over.")
            break

        reveal(r, c, board, visible, size)

        #check win
        unrevealed_safe = sum(1 for r_i in range(size) for c_i in range(size)
                              if not visible[r_i][c_i] != '*')
        if unrevealed_safe == 0:
            draw_board(board, visible, size)
            print("\nVictory! You cleared the field.")
            break
    
    input("\nPress Enter to return to Hub...")