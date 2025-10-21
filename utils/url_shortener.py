import urllib.parse
import requests
from requests.exceptions import RequestException


import os
from dotenv import load_dotenv

load_dotenv()


__api_base = "https://api.tinyurl.com"
__shorten_endpoint = f"{__api_base}/create"


def __validate_url(url: str) -> str:
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
    long_url = __validate_url(long_url)

    headers = {
        "Authorization": f"Bearer {os.getenv('TINYURL_API_TOKEN')}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "url": long_url,
        "domain": "tinyurl.com",
    }

    try:
        resp = requests.post(
            __shorten_endpoint, json=payload, headers=headers, timeout=timeout
        )
        resp.raise_for_status()
    except RequestException as e:
        raise RequestException(f"Network/API request failed: {e}")

    data = resp.json()
    if "data" in data and "tiny_url" in data["data"]:
        return data["data"]["tiny_url"]
    else:
        raise ValueError(f"Unexpected API response: {data!r}")
