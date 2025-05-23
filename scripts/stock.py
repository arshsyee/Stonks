import yfinance as yf
import time
from yfinance.exceptions import YFRateLimitError  # fixed import

MAX_TRIES = 3
BACKOFF = 60

def fetch_stock_data(ticker_obj, period="7d"):
    """
    Fetch historical stock data with retry/back-off on YFRateLimitError.
    """
    attempt = 0
    while attempt < MAX_TRIES:
        try:
            # single call, using the passed-in period
            return ticker_obj.history(period=period)
        except YFRateLimitError:
            attempt += 1
            wait = BACKOFF * attempt
            print(f"[{ticker_obj.ticker}] Rate-limited (attempt {attempt}/{MAX_TRIES}). Sleeping {wait}s…")
            time.sleep(wait)
    raise RuntimeError(f"[{ticker_obj.ticker}] failed after {MAX_TRIES} retries")

def main():
    """Main function to get user input and fetch stock data."""
    print("Program is running…")
    symbol = input("Enter stock ticker: ").strip().upper()
    ticker = yf.Ticker(symbol)
    hist = fetch_stock_data(ticker)  # safe fetch
    print(hist)  # or process it however you like

if __name__ == "__main__":
    main()

