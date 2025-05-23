import finnhub
import pandas as pd
import sys
from datetime import datetime

# ── Configuration ──
API_KEY = "d0i5os1r01ql18ms0go0d0i5os1r01ql18ms0gog"
client  = finnhub.Client(api_key=API_KEY)

# ── 1. Prompt user ──
search_term = input("Enter a search term: ").strip().lower()
if not search_term:
    print("No search term entered. Exiting.")
    sys.exit()

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

# Convert to epoch seconds (UTC)
start_ts = int(start_dt.replace(tzinfo=None).timestamp())
end_ts   = int(end_dt.replace(tzinfo=None).timestamp())

# ── 4. Fetch all general market news ──
news_items = client.general_news('general', min_id=None)

# ── 5. Filter by date and keyword ──
rows = []
for item in news_items:
    dt = item.get("datetime")
    if dt is None:
        continue
    if start_ts <= dt <= end_ts and search_term in item.get("headline", "").lower():
        rows.append({
            "Headline":   item.get("headline", ""),
            "Source":     item.get("source",""),
            "Issue date": datetime.utcfromtimestamp(dt).strftime("%Y-%m-%d %H:%M"),
            "URL":        item.get("url", ""),
            "Summary":    item.get("summary", "")
        })

# ── 6. Output or notify none found ──
if not rows:
    print(f"No articles found containing '{search_term}' between {from_str} and {to_str}.")
    sys.exit()

# ── 7. Build DataFrame ──
df = pd.DataFrame(rows)
print(df.to_string(index=False))

# ── 8. Save to CSV ──
csv_filename = f"news_{search_term.replace(' ', '_')}_{from_str}_to_{to_str}.csv"
df.to_csv(csv_filename, index=False)
print(f"\nSaved {len(df)} articles to {csv_filename}")
