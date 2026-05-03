import random
import os

def merge_left(row):
    """Slides and merges a single row to the left."""
    # 1. Remove zeros
    new_row = [i for i in row if i != 0]
    # 2. Merge identical numbers
    for i in range(len(new_row) - 1):
        if new_row[i] == new_row[i+1] and new_row[i] != 0:
            new_row[i] *= 2
            new_row[i+1] = 0
    # 3. Compress again
    new_row = [i for i in new_row if i != 0]
    # 4. Fill remaining space with zeros
    return new_row + [0] * (len(row) - len(new_row))

def is_game_over(board):
    """Checks if there are no more moves possible."""
    for r in range(4):
        for c in range(4):
            if board[r][c] == 0: return False # Space left
            if c < 3 and board[r][c] == board[r][c+1]: return False # Horizontal merge possible
            if r < 3 and board[r][c] == board[r+1][c]: return False # Vertical merge possible
    return True

def transpose(matrix):
    """Swaps rows and columns."""
    return [list(row) for row in zip(*matrix)]

def add_new_tile(board):
    """Adds a 2 or 4 to a random empty spot."""
    empty = [(r, c) for r in range(4) for c in range(4) if board[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        board[r][c] = 2 if random.random() < 0.9 else 4

def draw_board(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--- 2048 TERMINAL ---")
    for row in board:
        print("-" * 21)
        # Formats each number to be centered in a 4-character space
        print("|" + "|".join(f"{str(x).replace('0', ' '):^4}" for x in row) + "|")
    print("-" * 21)

def run():
    board = [[0] * 4 for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)
    
    while True:
        draw_board(board)
        cmd = input("Move (WASD) or 'Q' to quit: ").lower().strip()
        
        if cmd == 'q': break
        if cmd not in ['w', 'a', 's', 'd']: continue
        
        old_board = [row[:] for row in board]
        
        # LOGIC FOR DIRECTIONS
        if cmd == 'a': # Left
            board = [merge_left(row) for row in board]
        elif cmd == 'd': # Right
            board = [merge_left(row[::-1])[::-1] for row in board]
        elif cmd == 'w': # Up
            board = transpose(board)
            board = [merge_left(row) for row in board]
            board = transpose(board)
        elif cmd == 's': # Down
            board = transpose(board)
            board = [merge_left(row[::-1])[::-1] for row in board]
            board = transpose(board)
            
        if board != old_board:
            add_new_tile(board)
        
        if is_game_over(board):
            draw_board(board)
            print("\n!!! GAME OVER !!!")
            input("Press Enter to return to Hub...")
            break
