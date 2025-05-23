import sys
from datetime import datetime, date
import finnhub
import pandas as pd

API_KEY = "d0i5os1r01ql18ms0go0d0i5os1r01ql18ms0gog"
client  = finnhub.Client(api_key=API_KEY)

# 1. Prompt user
search_term = input("Enter a company ticker: ").strip().upper()
if not search_term:
    print("No ticker entered. Exiting.")
    sys.exit(1)

past_days_str = input("Enter the start date (YYYY-MM-DD): ").strip()
try:
    past_days = datetime.strptime(past_days_str, "%Y-%m-%d").date()
except ValueError:
    print(f"Date error: '{past_days_str}' is not in YYYY-MM-DD format.")
    sys.exit(2)

if past_days > date.today():
    print(f"Date error: '{past_days_str}' is in the future.")
    sys.exit(3)

# 2. Fetching data
try:
    company_news = client.company_news(
        search_term,
        _from=past_days.isoformat(),
        to=date.today().isoformat()
    )
except Exception as e:
    print(f"News fetch error: {e}")
    sys.exit(4)

# 3. Handle “no articles found” as its own case
if not company_news:
    print(f"No articles found for {search_term} from {past_days_str} to today.")
    sys.exit(0)

# 4. Build the DataFrame as before…
rows = []
for item in company_news:
    # (filtering / row-building code here)
    rows.append({
        "Headline":   item.get("headline", ""),
        "Source":     item.get("source", ""),
        "Issue date": pd.to_datetime(item.get("datetime"), unit="s"),
        "URL":        item.get("url", ""),
        "Summary":    item.get("summary", "")
    })


df = pd.DataFrame(rows)
print(df.to_string(index=False))

# ── 5. Save to CSV ──
csv_filename = f"news_{search_term.replace(' ', '_')}.csv"
df.to_csv(csv_filename, index=False)
print(f"\nSaved {len(df)} articles to {csv_filename}")