import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import re

FEEDS = [
    ("العراق", "https://news.google.com/rss/search?q=Iraq&hl=ar&gl=IQ&ceid=IQ:ar"),
    ("العالم", "https://news.google.com/rss/search?q=World&hl=ar&gl=IQ&ceid=IQ:ar"),
    ("رياضة", "https://news.google.com/rss/search?q=Sports&hl=ar&gl=IQ&ceid=IQ:ar"),
    ("تقنية", "https://news.google.com/rss/search?q=Technology&hl=ar&gl=IQ&ceid=IQ:ar")
]

news = []

for category, feed_url in FEEDS:
    try:
        request = urllib.request.Request(
            feed_url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            data = response.read()

        root = ET.fromstring(data)

        for item in root.findall("./channel/item")[:10]:
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            source = item.findtext("source", "Google News").strip()
            pub_date = item.findtext("pubDate", "").strip()
            description = item.findtext("description", "").strip()

            summary = re.sub("<[^>]+>", "", description).strip()
            summary = summary or title

            if title and link:
                news.append({
                    "title": title,
                    "category": category,
                    "summary": summary,
                    "source": source,
                    "url": link,
                    "image": "",
                    "date": pub_date,
                    "updated": datetime.now(timezone.utc).isoformat()
                })

    except Exception as e:
        print(f"فشل جلب {category}: {e}")

with open("news.json", "w", encoding="utf-8") as file:
    json.dump(news, file, ensure_ascii=False, indent=2)

print(f"تم جلب {len(news)} خبرًا.")
