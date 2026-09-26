import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import re
from html import unescape

FEEDS = [
    ("العراق", "https://news.google.com/rss/search?q=Iraq&hl=ar&gl=IQ&ceid=IQ:ar"),
    ("العالم", "https://news.google.com/rss/search?q=World&hl=ar&gl=IQ&ceid=IQ:ar"),
    ("رياضة", "https://news.google.com/rss/search?q=Sports&hl=ar&gl=IQ&ceid=IQ:ar"),
    ("تقنية", "https://news.google.com/rss/search?q=Technology&hl=ar&gl=IQ&ceid=IQ:ar")
]

NS = {
    "media": "http://search.yahoo.com/mrss/"
}

news = []

def clean_html(text):
    text = unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def find_image(item, description):
    media = item.find("media:content", NS)
    if media is not None:
        url = media.get("url", "")
        if url:
            return url

    thumb = item.find("media:thumbnail", NS)
    if thumb is not None:
        url = thumb.get("url", "")
        if url:
            return url

    match = re.search(
        r'<img[^>]+src=["\']([^"\']+)["\']',
        description or "",
        re.I
    )
    if match:
        return match.group(1)

    enclosure = item.find("enclosure")
    if enclosure is not None:
        url = enclosure.get("url", "")
        if url:
            return url

    return ""

for category, feed_url in FEEDS:
    try:
        request = urllib.request.Request(
            feed_url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()

        root = ET.fromstring(data)

        for item in root.findall("./channel/item")[:10]:
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            source = item.findtext("source", "Google News").strip()
            pub_date = item.findtext("pubDate", "").strip()

            description = item.findtext("description", "")
            summary = clean_html(description)

            if not summary:
                summary = title

            if len(summary) > 700:
                summary = summary[:700].rsplit(" ", 1)[0] + "..."

            image = find_image(item, description)

            if title and link:
                news.append({
                    "title": title,
                    "category": category,
                    "summary": summary,
                    "source": source,
                    "url": link,
                    "image": image,
                    "date": pub_date,
                    "updated": datetime.now(timezone.utc).isoformat()
                })

    except Exception as e:
        print(f"فشل جلب {category}: {e}")

with open("news.json", "w", encoding="utf-8") as file:
    json.dump(news, file, ensure_ascii=False, indent=2)

print(f"تم جلب {len(news)} خبرًا.")
