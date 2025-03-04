import yfinance as yf

def fetch_stock_data(ticker_obj):
    """Fetch historical stock data and other financial details."""
    print(f"\nFetching stock data for {ticker_obj.ticker}...")

    # Get historical stock prices
    hist = ticker_obj.history(period="7d")

    if hist.empty:
        print("⚠ No data retrieved! Check ticker symbol or internet connection.")
    else:
        hist = hist.sort_index(ascending=False)
        print("\nStock Price Data:\n", hist)
        print(f"\nTotal Entries: {len(hist)}")

    # Get Recommendations
    print("\nStock Recommendations:\n", ticker_obj.recommendations)

    # Get Major & Institutional Holders
    print("\nMajor Holders:\n", ticker_obj.major_holders)
    print("\nInstitutional Holders:\n", ticker_obj.institutional_holders)

def main():
    """Main function to handle user input and execute stock data retrieval."""
    print("Program is running...")
    
    ticker_symbol = input("Enter stock ticker: ").strip().upper()  # Get user input
    ticker_obj = yf.Ticker(ticker_symbol)  # ✅ Create a `yfinance.Ticker` object

    fetch_stock_data(ticker_obj)  # ✅ Pass the object to fetch stock data

# Runs when executed directly but allows function use when imported
if __name__ == "__main__":
    main()
