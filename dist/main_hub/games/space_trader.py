import random, os, time

#config
CONTRABAND = {"Narcotics": 400, "Gene-Sequences": 900, "Void-Tech": 1500}
GOODS = {"Water": 10, "O2": 30, "Microchips": 150, "Fuel":15 }

class Planet:
    def __init__(self, name): # Make sure there are TWO underscores on each side
        self.name = name
        # Prices fluctuate based on the planet
        self.prices = {
            "Water": random.randint(5, 20),
            "O2": random.randint(20, 50),
            "Microchips": random.randint(100, 250),
            "Fuel": random.randint(10, 25),
            "Narcotics": random.randint(300, 700),
            "Gene-Sequences": random.randint(800, 2000),
            "Void-Tech": random.randint(1500, 3500)
        }

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def police_minigame(wanted_level, bonus_time):
    clear()
    print(f"!!! POLICE SCAN DETECTED (Wanted Level: {wanted_level}) !!!")
    time_limit = max(1.2, 4.0 + bonus_time - wanted_level)
    print(f"You have {time_limit:.1f}s to scramble your signal")

    code = " ".join(random.choices("ABCD", k=min(6, 3 + wanted_level)))
    print(f"\nQUICK! ENTER THE CODE: {code}")

    start = time.time()
    user_input = input("> ").upper().strip()
    end = time.time()

    return user_input == code and (end - start) < time_limit

def start_race(stats):
    clear()
    print("--- ASTEROID RACE TRACK ---")
    if stats['credits'] <= 0:
        print("You're broke! (Bozo) No racing for you"); time.sleep(1); return
    
    try:
        bet = int(input(f"Enter your credit bet (Max {stats['credits']}): "))
        if bet > stats['credits'] or bet <= 0: return
    except ValueError: return

    print("\nSelect Difficulty:")
    print("1. Easy (Opponent Speed: 15) - 1.5x Payout")
    print("2. Medium (Opponent Speed: 25) - 3.0x Payout")
    print("3. Hard (Opponent Speed: 40) - 6.0x Payout")
    diff = input("> ")

    difficulty_map= {"1": (15, 1.5), "2": (25, 3.0), "3": (40, 6.0)}
    if diff not in difficulty_map: return

    opp_speed, multiploer = difficulty_map[diff]
    print("\n[RACING...]")
    time.sleep(2)

    your_perf = stats['speed'] + random.randint(1, 12)
    opp_perf = opp_speed + random.randint(1, 12)

    if your_perf >= opp_perf:
        winnings = int(bet * multiplier)
        stats['credits'] -= bet
        print(f"VICTORY! You won {winnings} credits!")
    else:
        stats['credits'] -= bet
        print(f"DEFEAT. You lost your bet of {bet} credits.")
    input("\nPress Enter to return...")

def generate_random_name():
    prefixes = ["Neo", "Alpha", "Dark", "Star", "Cloud", "Void", "Iron"]
    suffixes = [" Prime", " Station", " IX", " Alpha", " Outpost", "-V", " Delta"]
    return random.choice(prefixes) + random.choice(suffixes)

def run():

    planets = [Planet(generate_random_name()) for _ in range(20)]

    #int stats
    stats = {
        'credits': 500, 'fuel': 100, 'hp': 100, 'max_hp': 100,
        'shields': 50, 'max_shields': 50, 'attack': 10, 'speed': 10,
        'wanted_level': 0, 'smuggler_mod': 0, 'cargo_space': 10
    }
    current = random.choice(planets)
    cargo = {item: 0 for item in current.prices.keys()}

    while True:
        #pas shield regen
        stats['shields'] = min(stats['max_shields'], stats['shields'] + 5)
        has_contraband = any(cargo[c] > 0 for c in CONTRABAND)

        clear()
        print(f"--- {current.name.upper()} STATION --- Credits: {stats['credits']} | Wanted: {'*' * stats['wanted_level']}")
        print(f"Hull: {stats['hp']}{stats['max_hp']} | Shields: {stats['shields']}/{stats['max_shields']}")
        print(f"Cargo: {sum(cargo.values())}/{stats['cargo_space']} | Engines: {stats['speed']} Speed")
        print("-" * 55)

        print("1. Trade 2. Black Market 3. Shipyard 4. Asteroid Race 5. Travel Q. Quit")
        choice = input("> ")

        if choice == '1': #norm trade
            print("\n--- MARKET ---")
            for item in GOODS:
                print(f"- {item}: {current.prices[item]}c (In Hold: {cargo[item]})")
            cmd = input("\n(B)uy / (S)ell [Item Name] or (Back): ").lower().split()
            if len(cmd) > 1:
                action, item = cmd[0], cmd[1].capitalize()
                if item in current.prices:
                    if action == 'b' and stats['credits'] >= current.prices[item] and sum(cargo.values()) < stats['cargo_space']:
                        if item == "Fuel": stats['fuel'] = min(100, stats['fuel'] + 20)
                        else: cargo[item] += 1
                        stats['credits'] -= current.prices[item]
                elif action == 's' and cargo[item] > 0:
                    cargo[item] -= 1
                    tats['credits'] += current.prices[item]

        elif choice == '2': #black market
            print("\n--- BLACK MARKET ---")
            for item in CONTRABAND:
                print(f"- {item}: {current.prices[item]}c (In Hold: {cargo[item]})")
            cmd = input("\n(B)uy / (S)ell [Item Name]: ").lower().split()
            if len(cmd) > 1:
                action, item = cmd[0], cmd[1].title().replace("Void-Tech", "Void-Tech").replace("Gene-Sequences", "Gene-Sequences")
                #spec name for contra
                if "Gene" in item: item = "Gene-Sequences"
                if "Void" in item: item = "Void-Tech"

                if item in CONTRABAND:
                    if action == 'b' and stats['credits'] >= current.prices[item] and sum(cargo.values()) < stats['cargo_space']:
                        cargo[item] += 1
                        stats['credits'] -= current.prices[item]
                    elif action == 's' and cargo[item] > 0:
                        cargo[item] -= 1
                        stats['credits'] += current.prices[item]
        
        elif choice == '3': #Shipyard
            print("\n--- SHIPYARD ---")
            print(f"1. Plasma Cannon (+10 Atk) - 400c")
            print(f"2. Kinetic Shields (+50 max) - 500c")
            print(f"3. Hyper-Engines (+15 Speed) - 600c")
            print(f"4. Bribe Offical (-1 Wanted) - 300c")
            up = input("> ")
            if up == '1' and stats['credits'] >= 400:
                stats['attack'] += 10; stats['credits'] -= 400
            elif up == '2' and stats['credits'] >= 500:
                stats['max_shields'] += 50; stats['credits'] -= 500
            elif up == '3' and stats['credits'] >= 600:
                stats['speed'] += 15; stats['credits'] -= 600
            elif up == '4' and stats['credits'] >= 300 and stats['wanted_level'] > 0:
                stats['wanted_level'] -= 1; stats['credits'] -= 300

        elif choice == '4':
            start_race(stats)
        
        elif choice == '5': #travel
            if stats['fuel'] >= 20:
                stats['fuel'] -= 20
                scan_chance = 0.3 + (stats['wanted_level'] * 0.15)
                if has_contraband and random.random() < scan_chance:
                    if not police_minigame(stats['wanted_level'], stats['smuggler_mod']):
                        stats['wanted_level'] += 1
                        fine = 500 * stats['wanted_level']
                        stats['credits'] = max(0, stats['credits'] - fine)
                        for c in CONTRABAND: cargo[c] = 0
                        print(f"BUSTED! Fine: {fine}c. Contraband seized."); time.sleep(2)
            
                current = random.choice([p for p in planets if p != current])
                print(f"Traviling to {current.name}..."); time.sleep(1.5)
            else:
                print("Fuel low!"); time.sleep(1)
    
        elif choice.lower() == 'q': break