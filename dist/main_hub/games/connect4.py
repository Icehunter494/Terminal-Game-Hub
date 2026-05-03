import os
import random
import time

def create_board():
    return[[' ' for _ in range(7)] for _ in range(6)]

def print_board(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("  1   2   3   4   5   6   7")
    print("+---" * 7 + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * 7 + "+")

def get_next_open_row(board, col):
    for r in range(5, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def check_win(board, piece):
    #hori
    for r in range(6):
        for c in range(4):
            if all(board[r][c+i] == piece for i in range (4)): return True
    #vert
    for r in range(3):
        for c in range(7):
            if all(board[r+i][c] == piece for i in range(4)): return True
    #pos dia
    for r in range(3, 6):
        for c in range(4):
            if all(board[r-i][c+i] == piece for i in range(4)): return True
    #neg dia
    for r in range(3):
        for c in range(4):
            if all(board[r+i][c+i] == piece for i in range(4)): return True
    return False

def run():
    board = create_board()
    game_over = False
    turn = 0 #0 for play 1 for ai

    while not game_over:
        print_board(board)
        
        # --- PLAYER TURN ---
        if turn == 0:
            choice = input("Player (X) - Choose column (1-7) or 'Q': ").upper().strip()
            if choice == 'Q': break
            if not choice.isdigit() or not (1 <= int(choice) <= 7):
                continue # Invalid input? Just restart the loop
            
            col = int(choice) - 1
            row = get_next_open_row(board, col)
            
            if row is not None:
                board[row][col] = 'X'
                if check_win(board, 'X'):
                    print_board(board)
                    print("Player wins!")
                    game_over = True
                turn = 1 # Switch to AI
            else:
                print("Column full! Try again.")
                time.sleep(1)

        # --- AI TURN ---
        else:
            print("AI (O) is thinking...")
            time.sleep(1) # Gives the illusion of "thought"
            valid_cols = [c for c in range(7) if get_next_open_row(board, c) is not None]
            
            if valid_cols:
                col = random.choice(valid_cols)
                row = get_next_open_row(board, col)
                board[row][col] = 'O'
                
                if check_win(board, 'O'):
                    print_board(board)
                    print("AI wins!")
                    game_over = True
                turn = 0 # Switch back to Player
            else:
                game_over = True # Board is full

    input("\nPress Enter to return to hub...")