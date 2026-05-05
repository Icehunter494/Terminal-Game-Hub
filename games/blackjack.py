import curses
import random

suits = ["♠", "♥", "♦", "♣"]
values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10, "A": 11
}

#helper
def create_deck():
    return[(v, s) for v in values for s in suits]

def draw_card(deck):
    return deck.pop(random.randint(0, len(deck) - 1))

def hand_value(hand):
    total = sum(values[c[0]] for c in hand)
    aces = sum(1 for c in hand if c[0] == "A")

    while total > 21 and aces:
        total -= 10
        aces -= 1

    return total

#draw func
def draw_card_ui(stdscr, y, x, card, hidden=False):
    if hidden:
        stdscr.addstr(y, x, "[??]", curses.color_pair(3))
        return
    
    value, suit = card
    color = 2 if suit in ["♥", "♦"] else 1
    stdscr.addstr(y, x, f"[{value}{suit}]", curses.color_pair(color))

def draw_hand(stdscr, y, x, name, hand, hide_first=False):
    stdscr.addstr(y, x, name, curses.A_BOLD)

    for i, card in enumerate(hand):
        draw_card_ui(stdscr, y + 1, x + i * 5, card, hidden=(hide_first and i == 0))

    if not hide_first:
        stdscr.addstr(y + 2, x, f"Value: {hand_value(hand)}")

def run(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(False)

    curses.start_color()
    curses.use_default_colors()
    
    curses.init_pair(1, curses.COLOR_WHITE, -1)  # normal
    curses.init_pair(2, curses.COLOR_RED, -1)    # red cards
    curses.init_pair(3, curses.COLOR_YELLOW, -1) # hidden

    while True:
        deck = create_deck()
        random.shuffle(deck)

        player = [draw_card(deck), draw_card(deck)]
        dealer = [draw_card(deck), draw_card(deck)]

        player_turn = True
        result = ""

        #player turn
        while player_turn:
            stdscr.erase()

            stdscr.addstr(1, 5, "BLACKJACK", curses.A_BOLD)
            
            draw_hand(stdscr, 3, 5, "Dealer", dealer, hide_first=True)
            draw_hand(stdscr, 8, 5, "Player", player)

            stdscr.addstr(14, 5, "H = Hit | S = Stand | Q = Quit")

            stdscr.refresh()

            if hand_value(player) == 21:
                result = "BLACKJACK!"
                break
            if hand_value(player) > 21:
                result = "BUST! You lose."
                break

            key = stdscr.getch()

            if key in [ord('q')]:
                return
            
            if key in [ord('h')]:
                player.append(draw_card(deck))
            
            elif key in [ord('s')]:
                player_turn = False
            
        #dealer turn
        while hand_value(dealer) < 17 and hand_value(player) <= 21:
            dealer.append(draw_card(deck))

        #result
        if not result:
            p = hand_value(player)
            d = hand_value(dealer)

            if d > 21:
                result = "Dealer busts! You win!"
            elif p > d:
                result = "You win!"
            elif p < d:
                result = "Dealer wins."
            else:
                result = "Push (tie)"
        
        stdscr.erase()

        stdscr.addstr(1, 5, "FINAL RESULT", curses.A_BOLD)

        draw_hand(stdscr, 3, 5, "Dealer", dealer)
        draw_hand(stdscr, 8, 5, "Player", player)

        stdscr.addstr(14, 5, result, curses.A_BOLD)
        stdscr.addstr(16, 5, "R = Replay | Q = Quit")

        stdscr.refresh()

        while True:
            key = stdscr.getch()

            if key in [ord('q')]:
                return
            elif key in [ord('r')]:
                break