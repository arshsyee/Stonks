import requests

# Base API URL
BASE_URL = "https://api.quiverquant.com"  # Ensure this is the correct base URL

# Correct endpoint (Example: Congressional Trades)
ENDPOINT = "/beta/bulk/congresstrading"  # Ensure the correct path
url = BASE_URL + ENDPOINT  # Construct full API URL

# Send request without authentication (Testing)
response = requests.get(url)

# Check response
if response.status_code == 200:
    print("✅ API is public, response received:")
    print(response.json()[:5])  # Show first 5 results
elif response.status_code == 404:
    print("❌ API endpoint not found! Double-check the URL.")
elif response.status_code == 401:
    print("❌ API requires authentication. You need an API key.")
else:
    print(f"⚠ Error {response.status_code}: {response.text}")