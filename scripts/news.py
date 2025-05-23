import finnhub
import pandas as pd
import json
import sys
from datetime import datetime

# ── Configuration ──
API_KEY = "d0i5os1r01ql18ms0go0d0i5os1r01ql18ms0gog"
client = finnhub.Client(api_key=API_KEY)

# ── 1. Prompt for company symbol ──
symbol = input("What are we looking for today: ").strip().upper()
if not symbol:
    print("No symbol entered. Exiting.")
    sys.exit(1)
# Use symbol as search term for general news
search_term = symbol.lower()

# ── 2. Prompt date range ──
from_str = input("From date (YYYY-MM-DD): ").strip()
to_str   = input("To   date (YYYY-MM-DD): ").strip()

# ── 3. Validate dates ──
try:
    start_dt = datetime.strptime(from_str, "%Y-%m-%d")
    end_dt   = datetime.strptime(to_str,   "%Y-%m-%d")
except ValueError as e:
    print(f"Invalid date format: {e}. Use YYYY-MM-DD.")
    sys.exit(1)
if start_dt > end_dt:
    print("Error: From date must be before To date.")
    sys.exit(1)

# ── 4. Convert to epoch seconds ──
start_ts = int(start_dt.timestamp())
end_ts   = int(end_dt.timestamp())

# ── 5. Fetch news feeds ┚
# Company news is already filtered by date by the API
company_items = client.company_news(symbol, _from=from_str, to=to_str)
general_items = client.general_news('general', min_id=None)

# ── 6. Merge & de-duplicate ──
rows = []
seen_urls = set()

# Add company-specific news first
for item in company_items:
    url = item.get("url", "")
    if not url or url in seen_urls:
        continue
    seen_urls.add(url)
    dt = item.get("datetime")
    issue_date = datetime.utcfromtimestamp(dt).strftime("%Y-%m-%d %H:%M") if dt else None
    rows.append({
        "Symbol":     symbol,
        "Source":     item.get("source", ""),
        "Headline":   item.get("headline", ""),
        "Issue date": issue_date,
        "URL":        url,
        "Summary":    item.get("summary", "")
    })

# Add general market news, filtered by date and symbol
for item in general_items:
    dt = item.get("datetime")
    if dt is None or not (start_ts <= dt <= end_ts):
        continue
    headline = item.get("headline", "")
    if search_term not in headline.lower():
        continue
    url = item.get("url", "")
    if not url or url in seen_urls:
        continue
    seen_urls.add(url)
    issue_date = datetime.utcfromtimestamp(dt).strftime("%Y-%m-%d %H:%M")
    rows.append({
        "Symbol":     symbol,
        "Source":     item.get("source", ""),
        "Headline":   headline,
        "Issue date": issue_date,
        "URL":        url,
        "Summary":    item.get("summary", "")
    })

# ── 7. Exit if no articles found ──
if not rows:
    print(f"No articles found for '{symbol}' between {from_str} and {to_str}.")
    sys.exit(0)

# ── 8. Display and save ──
df = pd.DataFrame(rows)
print(df.to_string(index=False))

json_filename = f"news_{symbol}_{from_str}_to_{to_str}.json"
with open(json_filename, 'w') as f:
    json.dump(rows, f, indent=2)
print(f"\nSaved {len(rows)} articles to {json_filename}")