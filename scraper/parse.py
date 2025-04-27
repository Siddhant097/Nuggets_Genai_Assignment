import os
import json
from bs4 import BeautifulSoup

RAW_DIR = "data/raw"
PARSED_DIR = "data/parsed"

os.makedirs(PARSED_DIR, exist_ok=True)

def extract_info(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator='\n')
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return {
        "text": "\n".join(lines[:300])  # adjust this if needed
    }

for filename in os.listdir(RAW_DIR):
    if filename.endswith(".html"):
        path = os.path.join(RAW_DIR, filename)
        with open(path, "r", encoding="utf-8") as file:
            html = file.read()
            data = extract_info(html)

        output_file = os.path.join(PARSED_DIR, filename.replace(".html", ".json"))
        with open(output_file, "w", encoding="utf-8") as out:
            json.dump(data, out, indent=2, ensure_ascii=False)

        print(f"✅ Parsed and saved: {output_file}")
