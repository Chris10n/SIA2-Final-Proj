from flask import Flask, request, render_template_string, redirect, url_for, flash
import requests
import urllib.parse

app = Flask(__name__)
app.secret_key = "change-me-to-a-secret"  # change for production

API_ENDPOINT = "https://tinyurl.com/api-create.php"

TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>TinyURL Shortener</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    body{font-family:system-ui,Segoe UI,Roboto,Arial;display:flex;min-height:100vh;
         align-items:center;justify-content:center;background:#f6f7fb;margin:0}
    .card{background:white;padding:1.5rem;border-radius:12px;box-shadow:0 6px 20px rgba(30,40,60,0.08);width:min(720px,95%)}
    input[type=text]{width:100%;padding:0.75rem;border-radius:8px;border:1px solid #ddd}
    button{padding:0.6rem 1rem;border-radius:8px;border:0;background:#2563eb;color:white;font-weight:600}
    .result{margin-top:1rem;padding:0.75rem;background:#f3f4f6;border-radius:8px}
  </style>
</head>
<body>
  <div class="card">
    <h2>TinyURL Shortener</h2>
    <form method="post" action="{{ url_for('shorten') }}">
      <label for="long_url">Enter a URL to shorten</label><br>
      <input id="long_url" type="text" name="long_url" placeholder="https://example.com/very/long/path" value="{{ request.form.get('long_url','')|e }}" required>
      <div style="margin-top:0.7rem">
        <button type="submit">Shorten</button>
      </div>
    </form>

    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="result">
          {% for msg in messages %}
            <div>{{ msg|safe }}</div>
          {% endfor %}
        </div>
      {% endif %}
    {% endwith %}

    {% if short_url %}
      <div class="result">
        Short URL: <a href="{{ short_url }}" target="_blank" rel="noopener noreferrer">{{ short_url }}</a>
        <div style="margin-top:0.5rem">
          <button onclick="navigator.clipboard.writeText('{{ short_url }}')">Copy</button>
        </div>
      </div>
    {% endif %}

    <p style="color:#666;margin-top:1rem;font-size:0.9rem">Powered by TinyURL API</p>
  </div>
</body>
</html>
"""

def validate_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        raise ValueError("Empty URL")
    if "://" not in url:
        url = "http://" + url
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Invalid URL scheme")
    return url

@app.route("/", methods=["GET"])
def index():
    return render_template_string(TEMPLATE)

@app.route("/", methods=["POST"])
def shorten():
    long_url = request.form.get("long_url", "")
    try:
        long_url = validate_url(long_url)
    except ValueError as e:
        flash(f"Invalid URL: {e}")
        return render_template_string(TEMPLATE, short_url=None)

    try:
        resp = requests.get(API_ENDPOINT, params={"url": long_url}, timeout=5.0)
        resp.raise_for_status()
    except Exception as e:
        flash(f"Failed to contact TinyURL API: {e}")
        return render_template_string(TEMPLATE, short_url=None)

    short = resp.text.strip()
    if not short.startswith("http"):
        flash(f"Unexpected API response: {short}")
        return render_template_string(TEMPLATE, short_url=None)

    return render_template_string(TEMPLATE, short_url=short)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
