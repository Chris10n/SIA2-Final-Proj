import requests
import json
import sys

if len(sys.argv) < 2:
    print("Usage: python shortener.py '{\"token\": \"YOUR_TOKEN\", \"longURL\": \"YOUR_URL\"}'")
    sys.exit(1)

try:
    args = json.loads(sys.argv[1])
    API_TOKEN = args["token"]
    long_url = args["longURL"]
except (json.JSONDecodeError, KeyError) as e:
    print("Invalid JSON input or missing keys. Make sure to include 'token' and 'longURL'.")
    sys.exit(1)

API_URL = "https://api.tinyurl.com/create"
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}
data = {
    "url": long_url,
    "domain": "tinyurl.com"
}

print("\nShortening your URL... please wait.")
response = requests.post(API_URL, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    tiny_url = result["data"]["tiny_url"]
    print(f"\nSuccess!\nOriginal URL: {long_url}\nShortened URL: {tiny_url}\n")
else:
    print("\nFailed to shorten URL.")
    print(f"Status Code: {response.status_code}")
    try:
        print("Error details:", json.dumps(response.json(), indent=2))
    except:
        print("Error:", response.text)
