# test_scraper.py
import pytest
from politician import scrape_trades_for

@pytest.fixture(scope="module")
def aapl_data():
    # we fetch once for all tests to save time
    data = scrape_trades_for("AAPL", headless=True, timeout=15)
    return data

def test_returns_list(aapl_data):
    assert isinstance(aapl_data, list), "Expected a list of trades"
    assert len(aapl_data) > 0, "Expected at least one trade row for AAPL"

def test_each_row_has_expected_keys(aapl_data):
    expected = {"Politician", "Issuer", "Date", "Type", "Size", "Price"}
    # adapt capitalization if your header names differ
    keys = set(aapl_data[0].keys())
    missing = expected - keys
    assert not missing, f"Missing columns in output: {missing}"

def test_filtering_by_ticker(aapl_data):
    issuers = {row["Issuer"] for row in aapl_data}
    assert "AAPL" in issuers, "Ticker filter didn’t return any rows for AAPL"
