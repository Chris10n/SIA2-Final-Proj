import requests
import json

long_url = input("Enter the URL you want to shorten: ").strip()

API_URL = "https://api.tinyurl.com/create"
API_TOKEN = "aK9n4WR0pqaDOmBenU83JIFuqgI67G412sDwSO4hVB2Bb5IPbNimTHZreG5L"

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
