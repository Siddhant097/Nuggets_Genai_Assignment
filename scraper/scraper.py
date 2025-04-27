
import os
import requests
from bs4 import BeautifulSoup
import urllib3

# Disable SSL warnings for unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 1. List of resolved restaurant URLs
RESTAURANTS = [
    'https://www.eatfit.in/',
    'https://www.mcdonalds.com/',
    'https://www.motimahaldelux.com/post/moti-mahal-lucknow',
    'https://www.nicicecreams.com/',
    'https://www.burgerking.com/',
    'https://www.barista.co.in/',
    'https://www.subway.com/',
    'https://lakhnaviswaad.com/',
    
]

# 2. Output directory for raw HTML
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')


def fetch_page(url):
    """Fetch a single page; return HTML or None on error (ignoring SSL cert issues)."""
    try:
        resp = requests.get(url, timeout=10, verify=False)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def save_raw(name, html):
    """Write raw HTML to data/raw/{name}.html."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{name}.html"
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


if __name__ == '__main__':
    print("🔍 Starting scraper...")
    for url in RESTAURANTS:
        html = fetch_page(url)
        if html:
            name = url.split('//')[-1].replace('/', '_').rstrip('_')
            save_raw(name, html)
            print(f"✅ Saved raw HTML for {url}")
        else:
            print(f"❌ Skipped {url} due to fetch error.")


