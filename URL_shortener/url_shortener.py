import urllib.parse
import requests
from requests.exceptions import RequestException

API_ENDPOINT = "https://tinyurl.com/api-create.php"

def validate_url(url: str) -> str:
    url = url.strip()
    if not url:
        raise ValueError("Empty URL")
    if "://" not in url:
        url = "http://" + url
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http/https URLs are supported")
    return url

def shorten_tinyurl(long_url: str, timeout: float = 5.0) -> str:
    long_url = validate_url(long_url)
    params = {"url": long_url}
    try:
        resp = requests.get(API_ENDPOINT, params=params, timeout=timeout)
        resp.raise_for_status()
    except RequestException as e:
        raise RequestException(f"Network/API request failed: {e}")
    short_url = resp.text.strip()
    if not short_url.startswith("http"):
        raise ValueError(f"Unexpected API response: {short_url!r}")
    return short_url

if __name__ == "__main__":
    long_url = input("Enter a URL to shorten: ").strip()
    try:
        short = shorten_tinyurl(long_url)
        print(f"Shortened URL: {short}")
    except Exception as e:
        print(f"Error: {e}")
