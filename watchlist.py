import json
from pathlib import Path


WATCHLIST_FILE = Path("watchlist.json")


def load_watchlist():
    if not WATCHLIST_FILE.exists():
        return []

    with open(WATCHLIST_FILE, "r") as file:
        return json.load(file)


def save_watchlist(watchlist):
    with open(WATCHLIST_FILE, "w") as file:
        json.dump(watchlist, file, indent=4)


def add_to_watchlist(symbol):
    symbol = symbol.upper().strip()

    watchlist = load_watchlist()

    if symbol != "" and symbol not in watchlist:
        watchlist.append(symbol)
        save_watchlist(watchlist)

    return watchlist


def remove_from_watchlist(symbol):
    symbol = symbol.upper().strip()

    watchlist = load_watchlist()

    if symbol in watchlist:
        watchlist.remove(symbol)
        save_watchlist(watchlist)

    return watchlist