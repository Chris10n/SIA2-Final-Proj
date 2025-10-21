from url_shortener import shorten_tinyurl

if __name__ == "__main__":
    long_url = input("Enter the URL to shorten: ").strip()

    try:
        short = shorten_tinyurl(long_url)
        print(f"Shortened URL: {short}")
    except Exception as e:
        print(f"Error: {e}")
