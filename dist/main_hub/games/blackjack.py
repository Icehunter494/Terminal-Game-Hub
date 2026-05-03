import random
import os
import time

def calculate_score(hand):
    """Calculates the score of a hand, handling Aces as 1 or 11"""
    score = 0
    aces =  0
    for card in hand:
        if card in ['J', 'Q', 'K']:
            score += 10
        elif card == 'A':
            aces += 1
            score += 11
        else:
            score += card

    #if score over 21 and have ace it turns into 1
    while score > 21 and aces:
        score -= 10
        aces -= 1
    
    return score

def draw_table(player_hand, dealer_hand, show_dealer=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--- BLACKJACk ---")

    #dealer hand
    if show_dealer:
        print(f"\nDealer's Hand: {dealer_hand} (Score: {calculate_score(dealer_hand)})")
    else:
        print(f"\nDealer's Hand: [{dealer_hand[0]}, ?]")
    
    #player hand
    print(f"\nYour Hand: {player_hand} (Score: {calculate_score(player_hand)})")
    print("-" * 25)

def run():
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4
    random.shuffle(deck)

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    game_over = False

    # player turn
    while calculate_score(player_hand) < 21:
        draw_table(player_hand, dealer_hand)
        choice = input("Do you want to (h)it or (s)tay?").lower().strip()

        if choice == 'h':
            player_hand.append(deck.pop())
        elif choice == 's':
            break
    player_score = calculate_score(player_hand)

    #dealer turn
    if player_score <= 21:
        while calculate_score(dealer_hand) < 17:
            draw_table(player_hand, dealer_hand, show_dealer=True)
            print("Dealer is hitting...")
            time.sleep(1.5)
            dealer_hand.append(deck.pop())

        dealer_score = calculate_score(dealer_hand)
        draw_table(player_hand, dealer_hand, show_dealer=True)


        #result
        if player_score > 21:
            print("\nYou BUSTED! Dealer wins.")
        elif dealer_score > 21:
            print("\nDealer BUSTED! You win!")
        elif player_score > dealer_score:
            print("\nYou win")
        elif player_score < dealer_score:
            print("\nDealer wins.")
        else:
            print("\nIt's a Push (Tie)")
        
        input("\nPress Enter to return to hub")