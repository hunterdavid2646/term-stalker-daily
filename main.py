import requests
import re
from datetime import date
from collections import Counter

# Simple RSS/Atom feed list (replace with any feeds)
FEEDS = [
    "https://hnrss.org/newest?q=AI",
    "https://www.reddit.com/r/artificial/.rss",
]

# Basic pattern for AI-related terms (models, products, repos)
TERM_PATTERN = re.compile(r'\b([A-Z][A-Za-z0-9-]{2,})\b')

# Keywords that indicate novelty (adjust as needed)
NOVEL_HINTS = ["launch", "release", "new", "introduc", "announc", "update"]

def fetch_feed(url):
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            # crude strip of XML tags to get text
            text = re.sub(r'<[^>]+>', ' ', r.text)
            return text
    except:
        return ''

def extract_terms(text):
    # Split into sentences and only keep those with novelty hints
    sentences = re.split(r'(?<=[.!?])\s+', text)
    candidates = []
    for s in sentences:
        if any(h in s.lower() for h in NOVEL_HINTS):
            candidates.extend(TERM_PATTERN.findall(s))
    # Filter common English words (simple heuristic)
    stopwords = {"The", "And", "For", "New", "AI", "API", "This", "That", "With", "From", "What", "How", "Why"}
    return [c for c in candidates if c not in stopwords and len(c) > 2]

def main():
    all_terms = []
    for url in FEEDS:
        data = fetch_feed(url)
        if data:
            all_terms.extend(extract_terms(data))

    # Count and sort by frequency
    counter = Counter(all_terms)
    top = counter.most_common(10)

    print(f"Daily AI Term Radar - {date.today().isoformat()}")
    print("="*40)
    if not top:
        print("No new terms detected today.")
    else:
        for term, count in top:
            print(f"{term}: {count}")

if __name__ == "__main__":
    main()
