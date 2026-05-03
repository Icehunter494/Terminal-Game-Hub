import random

# all 15 gest
GESTURES = [
    "Rock", "Fire", "Scissors", "Snake", "Human", "Wolf",
    "Sponge", "Paper", "Air", "Water", "Dragon", "Devil",
    "Lightning", "Gun", "Tree"
]
#setting what beats what
RULES = {
    "Rock": {"Fire":"pounds out", "Scissors": "crushes", "Snake": "crushes", "Human": "crushes", "Wolf": "crushes", "Tree": "blocks growth of"},
    "Fire": {"Scissors": "melts", "Paper": "burns", "Snake": "burns", "Humans": "burns", "Tree": "burns", "Wolf": "burns", "Sponge": "burns"},
    "Scissors": {"Air": "swish through", "Tree": "carve", "Paper": "cut", "Snake": "cut", "Human": "cut", "Wolf": "cut", "Sponge": "cut"},
    "Snake": {"Human": "bites", "Wolf": "bites", "Sponge": "swallows", "Tree": "nests in", "Paper": "nests", "Air": "breathes", "Water": "drinks"},
    "Human": {"Tree": "plants", "Wolf": "tames", "Sponge": "cleans with", "Paper": "writes", "Air": "breathes", "Water": "drinks", "Dragon": "slays"},
    "Tree": {"Wolf": "shelters", "Dragon": "shelters", "Sponge": "outlives", "Paper":"becomes", "Air": "produces", "Water": "drinks", "Devil": "imprisons"},
    "Wolf": {"Sponge": "chews up", "Paper": "chews up", "Air": "breathes", "Water": "drinks", "Dragon": "outruns", "Lightning": "outrun", "Devil": "bites heiny of"},
    "Sponge": {"Paper": "soaks", "Air": "uses pockets of", "Water": "absorbs", "Devil": "cleanses", "Dragon": "cleanses", "Gun": "cleans", "Lightning": "conducts"},
    "Paper": {"Air": "fans", "Rock": "covers", "Water": "floats on", "Devil": "rebukes", "Dragon": "rebukes", "Gun": "outlaws", "Lightning": "defines"},
    "Air": {"Fire": "blows out","Rock": "erodes", "Water": "evaporates", "Devil": "chokes", "Guns": "tarnishes", "Dragon": "freezes", "Lightning": "creates"},
    "Water": {"Devil": "drowns", "Dragon": "drowns", "Rock": "erodes", "Fire":"puts out", "Scissors": "rusts", "Gun": "rusts", "Lightning": "cpmdicts"},
    "Dragon": {"Devil": "commands", "Lightning": "breathes", "Fire": "breathes", "Rock": "rests on", "Scissors": "is immune to", "Gun": "is immune to", "Snake": "spawns"},
    "Devil": {"Rock": "hurls", "Fire": "breathes", "Scissors": "is immune to", "Gun": "is immune to", "Lightning": "casts", "Snake": "eats", "Human": "possesses"},
    "Lightning": {"Gun": "melts", "Dragon":"strikes", "Devil": "strikes", "Tree": "strikes", "Fire": "starts", "Rock": "spilts", "Scissors": "melts"},
    "Gun": {"Rock": "targets", "Scissors": "outclasses", "Fire": "extinguishes", "Human": "shoots", "Wolf": "shoots", "Tree": "shreds", "Snake": "kills"},
}

def run():
    print("--- Welcome to the ---")
    print("--- ULTIMATE ---")
    print("--- Rock Paper Scissors! ---")
    print(f"Options: {', '.join(GESTURES)}\n")

    while True:
        user_input = input("Choose your gesture (or 'Quit' to stop): ").capitalize()

        if user_input == "Quit":
            break
        if user_input not in GESTURES:
            print("Invalid gesture! Please pick from the list.")
            continue
        
        computer_choice = random.choice(GESTURES)
        print(f"Computer chose: {computer_choice}")

        if user_input == computer_choice:
            print(f"Tie! Both players chose {user_input}.")
        elif computer_choice in RULES[user_input]:
            verb = RULES[user_input][computer_choice]
            print(f"You Win! {user_input} {verb} {computer_choice}.")
        else:
            # Added .get() here to prevent crashes if a rule is missing
            verb = RULES[computer_choice].get(user_input, "beats")
            print(f"You Lose! {computer_choice} {verb} {user_input}.")
        print("-" * 30)