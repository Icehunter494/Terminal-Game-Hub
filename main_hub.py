import os
import importlib
import inspect
import sys   


if hasattr(sys, '_MEIPASS'):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.abspath(".")

GAMES_FOLDER = os.path.join(BASE_PATH, "games")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


#autoload
def load_games():
    games = []

    for file in os.listdir(GAMES_FOLDER):
        if file.endswith(".py") and file != "__init__.py":
            module_name = file[:-3]

            try:
                module = importlib.import_module(f"{GAMES_FOLDER}.{module_name}")

                # Clean display name
                name = getattr(
                    module,
                    "GAME_NAME",
                    module_name.replace("_", " ").title()
                )

                # Priority: run_game()
                if hasattr(module, "run_game"):
                    games.append((name, module.run_game))

                # Fallback: run()
                elif hasattr(module, "run"):
                    func = module.run
                    params = inspect.signature(func).parameters

                    if len(params) == 1:
                        # curses game → wrap it automatically
                        def wrapper(f=func):
                            import curses
                            curses.wrapper(f)
                        games.append((name, wrapper))
                    else:
                        # normal game
                        games.append((name, func))

            except Exception as e:
                print(f"Failed to load {module_name}: {e}")

    return games

#main menu

def main_menu():
    while True:
        clear_screen()

        games = load_games()

        print("=== TERMINAL GAME HUB ===\n")

        for i, (name, _) in enumerate(games, 1):
            print(f"{i}. {name}")

        print("\nSelect a number to launch a game")
        print("Q. Quit")

        choice = input("\n> ").strip().lower()

        if choice == 'q':
            print("Shutting down...")
            break

        if choice.isdigit():
            idx = int(choice) - 1

            if 0 <= idx < len(games):
                name, game_func = games[idx]

                print(f"\nLoading {name}...")

                try:
                    game_func()
                except Exception as e:
                    print(f"Game crashed: {e}")

                input("\nPress Enter to return to menu...")
            else:
                input("Invalid selection. Press Enter...")

        else:
            input("Invalid input. Press Enter...")

#entry
if __name__ == "__main__":
    main_menu()