# smoke_test.py
from politician import scrape_trades_for

if __name__ == "__main__":
    ticker = "AAPL"
    data = scrape_trades_for(ticker, headless=True, timeout=15)
    assert isinstance(data, list), "❌ Expected a list"
    assert len(data) > 0,      "❌ No rows returned"
    issuers = {row["Issuer"] for row in data}
    assert ticker in issuers,  f"❌ '{ticker}' not in result issuers: {issuers}"
    print("✅ scraper.py smoke test passed: returned", len(data), "rows for", ticker)
