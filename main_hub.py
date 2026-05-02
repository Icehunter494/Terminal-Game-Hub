import os
from games import rps_15, mad_libs, bullet_hell, roguelike, battleship, game_2048





def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    #start func
    game_map = {
        "1": ("Rock Paper Scissors", rps_15.run),
        "2": ("Madlibs", mad_libs.run),
        "3": ("Bullet Hell", bullet_hell.run),
        "4": ("Dungeon Crawler", roguelike.run),
        "5": ("Battleship", battleship.run),
        "6": ("2048", game_2048.run)
    }

    while True:
      clear_screen()
      print("--- Hi! ---")
      for key, (name, _) in game_map.items():
         print(f"{key}. {name}")
      print("Q to quit")

      choice = input("\nSelect a game to load: ").strip().upper()

      if choice == 'Q':
            print("Shutting down...")
            break
      elif choice in game_map:
          print(f"Loading {game_map[choice][0]}...")
          #calls run
          game_map[choice][1]()
          input("\nGame Over. Press Enter to return to Hub...")
      else:
          print("Invalid selection.")

if __name__ == "__main__":
    main_menu()