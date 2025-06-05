import os
import requests
import json
import pandas as pd

# ── Configuration ──
# (Optional) Sign up for an API key at https://api.congress.gov and set it:
# export CONGRESS_API_KEY="your_key_here"
CONGRESS_API_KEY = "9bhwj12hOhleCPyMxjSL6CXXWOyTyzzCzzaXedmz"

# ── API Endpoints ──
HOUSE_TX_URL = (
    "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json"
)
SENATE_TX_URL = (
    "https://senate-stock-watcher-data.s3-us-west-2.amazonaws.com/aggregate/all_transactions.json"
)


def fetch_transactions(url: str) -> list:
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def filter_by_ticker(transactions: list, ticker: str) -> list:
    return [tx for tx in transactions if tx.get("ticker", "").upper() == ticker]


def fetch_current_members() -> dict:
    """
    Stub: return a mapping of MEMBER_NAME -> {party, state}
    """
    return {}


def main():
    # 1) Ask user for ticker
    ticker = input("Ticker (e.g. AAPL): ").strip().upper()

    # 2) Fetch raw transactions
    house_tx = fetch_transactions(HOUSE_TX_URL)
    senate_tx = fetch_transactions(SENATE_TX_URL)

    # 3) Filter for our ticker
    raw = filter_by_ticker(house_tx, ticker) + filter_by_ticker(senate_tx, ticker)
    if not raw:
        print(f"No trades found for {ticker}")
        return

    # 4) Load into DataFrame
    df = pd.DataFrame(raw)

    # 5) Annotate: create member_name from representative/senator
    rep_series = df["representative"] if "representative" in df.columns else pd.Series([None]*len(df), index=df.index)
    sen_series = df["senator"]        if "senator"      in df.columns else pd.Series([None]*len(df), index=df.index)
    df["member_name"] = rep_series.fillna(sen_series).fillna("")

    # 6) Combine and parse dates (mixed formats)
    date_series = df.get("transaction_date", pd.Series([None]*len(df), index=df.index))
    disc_series = df.get("disclosure_date",     pd.Series([None]*len(df), index=df.index))
    df["transaction_date"] = pd.to_datetime(date_series.fillna(disc_series), errors='coerce')

    # 7) Rename fields for consistency
    df.rename(columns={"amount": "amount_range", "asset_description": "asset"}, inplace=True)

    # 8) Optionally enrich with party/state
    members = fetch_current_members()
    if members:
        df["party"] = df["member_name"].str.upper().map(lambda n: members.get(n, {}).get("party"))
        df["state"] = df["member_name"].str.upper().map(lambda n: members.get(n, {}).get("state"))
    else:
        df["party"] = None
        df["state"] = None

    # 9) Sort by date
    df.sort_values("transaction_date", inplace=True)

    # 10) Convert timestamps to ISO strings for JSON
    df["transaction_date"] = df["transaction_date"].dt.strftime("%Y-%m-%d")

    # 11) Split into buys/sells
    df_buys  = df[df["type"].str.lower() == "purchase"]
    df_sells = df[df["type"].str.lower() == "sale"]

    buys  = df_buys.to_dict(orient="records")
    sells = df_sells.to_dict(orient="records")
    trades_sorted = df.to_dict(orient="records")

    # 12) Build summary object
    summary = {
        "ticker":       ticker,
        "total_trades": len(trades_sorted),
        "num_buys":     len(buys),
        "num_sells":    len(sells),
        "buys":         buys,
        "sells":        sells,
        "trades":       trades_sorted
    }

    # 13) Write JSON + CSV
    json_file = f"{ticker}_trades.json"
    with open(json_file, "w", encoding="utf-8") as jf:
        json.dump(summary, jf, indent=2, ensure_ascii=False)

    csv_file = f"{ticker}_trades_detailed.csv"
    df.to_csv(csv_file, index=False)

    # 14) Output
    print(json.dumps(summary, indent=2))
    print(f"\nWrote JSON ({json_file}) and sorted CSV ({csv_file}) for {ticker}")

if __name__ == "__main__":
    main()
