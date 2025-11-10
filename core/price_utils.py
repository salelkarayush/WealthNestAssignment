import json
import os

# Path to your JSON file
PRICES_FILE_PATH = os.path.join(os.path.dirname(__file__), "../data/prices.json")

# Cache prices after first load
_prices_cache = None


def load_prices():
    global _prices_cache
    if _prices_cache is None:
        try:
            with open(PRICES_FILE_PATH, "r") as file:
                _prices_cache = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Price data file not found at {PRICES_FILE_PATH}")
    return _prices_cache


def get_mock_price(symbol: str) -> float | None:
    """Returns the price for the given symbol from local JSON."""
    prices = load_prices()
    price = prices.get(symbol.upper())
    return float(price) if price is not None else None
