import random
import os
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Planet:
    def __init__(self, name):
        self.name = name
        #price change per planet
        self.prices = {
            "Fuel": random.randint(10, 20),
            "Water": random.randint(5, 15),
            "O2": random.randint(20, 40),
            "Microchips": random.randint(100, 200)

        }

def run():
    #universe
    names = ["Xylos", "Nova", "Terra", "Phoros", "Krypton", "Iceland"]
    planets = [Planet(name) for name in names]
    current_planet = random.choice(planets)

    #player stats
    credits = 500
    fuel = 100
    cargo = {"Water": 0, "O2": 0, "Microchips": 0}
    max_cargo = 10

    while True:
        clear()
        print(f"--- SPACE TRADER: STATION {current_planet.name.upper()}---")
        print(f"Credits: {credits} | Fuel: {fuel}% | Cargo: {sum(cargo.values())}/{max_cargo}")
        print("-" * 40)

        #dis prices
        for item, price in current_planet.prices.items():
            print(f"- {item}: {price} Credits")
        
        print("\nCommands: (b)uy [Item], (s)ell [Item], (t)ravel, (q)uit")
        choice = input("> ").lower().split()

        if not choice: continue
        action = choice[0]

        if action == 'q': break

        #buy logic
        elif action == 'b' and len(choice) > 1:
            item = choice[1].capitalize()
            if item in current_planet.prices:
                price = current_planet.prices[item]
                if credits >= price and sum(cargo.values()) < max_cargo:
                    if item == "Fuel":
                        fuel = min(100, fuel + 10)
                    else:
                        cargo[item] += 1
                    credits -= price
                else:
                    print("Not enough credits or cargo space!")
                    time.sleep(1)
        
        #sell logic
        elif action == 's' and len(choice) > 1:
            item = choice[1].capitalize()
            if item in cargo and cargo[item] > 0:
                credits += current_planet.prices[item]
                cargo[item] -= 1
            else:
                print("You don't have any of that!")
                time.sleep(1)
        
        #travel logic
        elif action == 't':
            if fuel >= 20:
                destination = [p for p in planets if p != current_planet]
                print("\nWhere to?")
                for i, p in enumerate(destination):
                    print(f"{i+1}. {p.name}")
                
                dest_choice = input("Enter number: ")
                if dest_choice.isdigit() and 0 < int(dest_choice) <= len(destination):
                    current_planet = destination[int(dest_choice)-1]
                    fuel -= 20
                    print(f"Hyperjumping to {current_planet.name}...")
                    time.sleep(1.5)
            else:
                print("Not enough fuel")
                time.sleep(1)
        
input("\nReturning to Hub. Press Enter...")