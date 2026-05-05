import os
import random

#util

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#color
COLORS = ["R", "G", "B", "Y", "O", "P"]

#gen secr
def generate_code(length):
    return [random.choice(COLORS) for _ in range(length)]

#eval guess

def evaluate(secret, guess):
    black = 0
    white = 0

    temp_secret = secret[:]
    temp_guess = guess[:]

    #black peg crrt pos
    for i in range(len(secret)):
        if guess[i] == secret[i]:
            black += 1
            temp_secret[i] = None
            temp_guess[i] = None
    
    #white peg crrt color wrg pos
    for i in range(len(guess)):
        if temp_guess[i] and temp_guess[i] in temp_secret:
            white += 1
            temp_secret[temp_secret.index(temp_guess[i])] = None
        
        return black, white
    
#display
def show_board(history):
    print("\nGuess History:")
    print("-" * 30)

    for guess, (b, w) in history:
        print(f"{' '.join(guess)} | Black: {b} White: {w}")

#main game
def run():
    while True:
        clear()
        print("=== MASTERMIND ===\n")

        print("Choose difficulty:")
        print("1. Easy (4 pegs)")
        print("2. Medium (5 pegs)")
        print("3. Hard (6 pegs)")
        print("Q. Quit")

        choice = input("\n> ").lower()

        if choice == 'q':
            return
        
        if choice == '1':
            length = 4
            attempts = 10
        elif choice == '2':
            length = 5
            attempts = 12
        elif choice == '3':
            length = 6
            attempts = 14
        else:
            continue

        secret = generate_code(length)
        history = []

        #game loop
        for turn in range(1, attempts + 1):
            clear()
            print(f"MASTERMIND ({turn}/{attempts})\n")
            
            print(f"Colors: {' '.join(COLORS)}")
            print(f"Enter {length} letters (e.g. RGBY)\n")

            show_board(history)

            guess_input = input("\nGuess: ").upper()

            #vali
            if len(guess_input) != length or any(c not in COLORS for c in guess_input):
                input("Invalid guess! Press Enter...")
                continue

            guess = list(guess_input)

            black, white = evaluate(secret, guess)
            history.append((guess, (black, white)))

            #win
            if black == length:
                clear()
                print("YOU CRACKED THE CODE!")
                print(f"Code was: {' '.join(secret)}")
                break
        
        else:
            clear()
            print("OUT OF ATTEMPTS!")
            print(f"Code was: {' '.join(secret)}")
        
        #replay
        again = input("\nPlay again? (y/n):").lower()
        if again != 'y':
            break