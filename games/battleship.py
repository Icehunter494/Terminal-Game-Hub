import random

def run():
    size = 10

    ship_grid = [['~' for _ in range(size)] for _ in range(size)]
    player_view = [['~' for _ in range(size)] for _ in range(size)]

    ships = {"Carrier": 5, "Battleship": 4, "Cruiser": 3, "Submarine": 3, "Destroyer": 2}
    total_hits_needed = sum(ships.values())
    hits = 0
    turns = 40 # number of missiles

    # random place ships
    for ship, length in ships.items():
        placed = False
        while not placed:
            orientation = random.choice(['H', 'V'])
            row = random.randint(0, size - 1)
            col = random.randint(0, size -1)

            #makes sure nun overlaps
            if orientation == 'H' and col + length <= size:
                if all(ship_grid[row][col+i] == '~' for i in range(length)):
                    for i in range(length): ship_grid[row][col+i] = 'S'
                    placed = True
                elif orientation == 'V' and row + length <= size:
                    if all(ship_grid[row+i][col]== '~' for i in range(length)):
                        for i in range(length): ship_grid[row+i][col] = 'S'
                        placed = True

    print("--- WELCOME TO BATTLESHIP ---")

    while hits < total_hits_needed and turns > 0:
        #dis board
        print("\n " + " ".join(str(i) for i in range(size)))
        for i, row in enumerate(player_view):
            print(f"{chr(65+i)}" + " ".join(row))
        
        print(f"\nHits: {hits}/{total_hits_needed} | Missiles left: {turns}")
        target = input("Enter target (e.g. A5) or 'Q' to quit: ").upper()

        if target == 'Q':break
        if len(target) < 2 or not target[0].isalpha() or not target[1:].isdigit():
            print("Invalid format! Use a letter and number (A0-J9)")
            continue
        
        r, c = ord(target[0]) - 65, int(target[1:])
        
        if r < 0 or r >= size or c < 0 or c >= size:
            print("Target out of bounds!")
            continue

        if player_view[r][c] != '~':
            print("You already fired there!")
            continue

        turns -= 1
        if ship_grid[r][c] == 'S':
            print("KABOOM! It's a Hit!")
            player_view[r][c] = 'X'
            hits += 1
        else:
            print("Splash... Miss.")
            player_view[r][c] = 'O'

    if hits == total_hits_needed:
        print("\nVICtORY! You sank the entire fleet!")
    else:
        print("\nDEFEAT. You ran out of missiles.")