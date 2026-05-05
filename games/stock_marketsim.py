import os
import random

#util

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#stock data
STOCKS = {
    "TECH":      {"price": 100, "vol": 8, "trend": 0},
    "ENERGY":    {"price": 80,  "vol": 6, "trend": 0},
    "FOOD":      {"price": 50,  "vol": 3, "trend": 0},
    "AI_CORP":   {"price": 120, "vol": 12, "trend": 0},
    "SPACE_INC": {"price": 150, "vol": 15, "trend": 0}
}

#market state
market_state = "NORMAL" #normal / bull / bear

#news events
NEWS_EVENTS = [
    ("Tech boom!", "TECH", +20),
    ("Oil crisis!", "ENERGY", -15),
    ("AI breakthrough!", "AI_CORP", +25),
    ("Food shortage!", "FOOD", +10),
    ("Space funding cuts!", "SPACE_INC", -20),
    ("Market crash!", None, -10),
    ("Investor hype!", None, +10),
]

#market update
def update_market():
    global market_state

    #random market shift
    if random.random() < 0.05:
        market_state = random.choice(["BULL", "BEAR", "NORMAL"])
    for name, data in STOCKS.items():
        #base movement
        change = random.randint(-data["vol"], data["vol"])

        #momentum
        change += data["trend"]

        #influence
        if market_state == "BULL":
            change += 3
        elif market_state == "BEAR":
            change -= 3

        #apply change
        data["price"] = max(5, data["price"] + change)

        #update trend
        data["trend"] = max(-5, min(5, data["trend"] + random.randint(-1, 1)))

#rand news event
def apply_news():
    if random.random() < 0.3:
        msg, target, impact = random.choice(NEWS_EVENTS)

        print(f"\nNEWS: {msg}")

        if target:
            STOCKS[target]["price"] = max(5, STOCKS[target]["price"] + impact)
        else:
            for s in STOCKS:
                STOCKS[s]["price"] = max(5, STOCKS[target]["price"] + impact)
        
        input("\nPress Enter...")

#display
def show_market(cash, portfolio, day):
    clear()

    print("=== STOCK MARKET SIM ===\n")
    print(f"Day: {day} | Market: {market_state}\n")

    print("STOCKS:")
    print("-" * 40)
    for name, data in STOCKS.items():
        trend = "↑" if data["trend"] > 0 else "↓" if data["trend"] < 0 else "-"
        print(f"{name:10} ${data['price']:4} | vol:{data['vol']} | trend:{trend}")
    
    print("\nPORTFOLIO:")
    print("-" * 40)

    if not portfolio:
        print("Empty")
    else:
        for name, qty in portfolio.items():
            value = STOCKS[name]["price"] * qty
            print(f"{name:10} x{qty} = ${value}")

#dividends
def pay_dividends(portfolio, cash):
    for stock, qty in portfolio.items():
        if random.random() < 0.2:
            payout = qty * random.randint(1, 5)
            cash += payout
            print(f"\nDividend from {stock}: +${payout}")

    return cash

#portfolio
def portfolio_value(portfolio):
    return sum(STOCKS[s]["price"] * q for s, q in portfolio.items())

#gameloop
def run():
    cash = 500
    portfolio = {}
    day = 1

    while True:
        update_market()
        apply_news()

        cash = pay_dividends(portfolio, cash)
        show_market(cash, portfolio, day)

        net = cash + portfolio_value(portfolio)
        print(f"\nNET WORTH: ${net}")

        print("\n1. Buy")
        print("2. Sell")
        print("3. Next Day")
        print("Q. Quit")

        choice = input("\n> ").lower()

        #quit
        if choice == "q":
            break

        #buy
        elif choice == "1":
            stock = input("Stock: ").upper()

            if stock in STOCKS:
                qty = int(int("Amount: "))
                cost = STOCKS[stock]["price"] * qty

                if cost <= cash:
                    cash -= cost
                    portfolio[stock] = portfolio.get(stock, 0) + qty
                else:
                    input("Not enough cash!")
            else:
                input("Invalid stock!")
# sell 
        elif choice == "2":
            stock = input("Stock: ").upper()

            if stock in portfolio:
                qty = int(input("Amount: "))

                if qty <= portfolio[stock]:
                    cash += STOCKS[stock]["price"] * qty
                    portfolio[stock] -= qty

                    if portfolio[stock] == 0:
                        del portfolio[stock]
                else:
                    input("You don't own that many!")
            else:
                input("You don't own that stock!")
    #next day
        elif choice == "3":
            day += 1
        
        else:
            input("Invalid choice!")
    
    clear()
    print("GAME OVER")
    print(f"Final Net Worth: ${cash + portfolio_value(portfolio)}")
    input("\nPress Enter...")