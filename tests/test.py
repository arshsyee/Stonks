import requests
from datetime import datetime

def fetch_bbc_headlines(api_key):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        #'sources': 'bbc-news',
        'q':'bitcoin',
        'pageSize':20,
        'apiKey': api_key
    }
    
    response = requests.get(url, params=params)     #checking if this piece of shit is working
    data = response.json()
    print(response)  # Debug print
    
    if data.get("status") != "ok":
        print("Error:", data.get("message", "Unknown error"))
        return

    articles = data.get("articles", [])

    if articles:
        for i, article in enumerate(articles, start=1):
            print(f"{i}. {article.get('title')}")
            print(f"    URL link:{article.get('url','No url')}")
            
            source_dict = article.get('source', {})
            source_name = source_dict.get('name', 'No source')
            print(f"    Source: {source_name}")
            
            date_str = article.get('publishedAt')
            if date_str:
                date_str = date_str.replace('Z','+00:00')
                published_dt = datetime.fromisoformat(date_str)
                date = published_dt.strftime('%Y-%m-%d %H:%M:%S UTC')
                print(f"    Published: {date}")
            else:
                print(f"    Date unavailable.")

            print("---------")
    else:
        print("No headlines found.")

if __name__ == "__main__":
    fetch_bbc_headlines("915d9c51765c46bdae8c6089c0afac16")