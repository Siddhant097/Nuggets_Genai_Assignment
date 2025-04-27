import re

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    return text.strip()

def print_chat(query, response):
    print(f"\n🧑‍💬 User: {query}")
    print(f"🤖 Bot: {response}\n")

def truncate_text(text, max_words=100):
    words = text.split()
    if len(words) > max_words:
        return " ".join(words[:max_words]) + "..."
    return text
