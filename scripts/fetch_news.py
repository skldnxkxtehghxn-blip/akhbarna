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
    "media": "http://search.yahoo.com/mrss/",
    "content": "http://purl.org/rss/1.0/modules/content/"
}

news = []

def clean_html(text):
    text = unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def find_image(item, description):
    # محاولة أخذ الصورة من media:content
    media = item.find("media:content", NS)
    if media is not None:
        url = media.get("url", "")
        if url:
            return url

    # محاولة media:thumbnail
    thumb = item.find("media:thumbnail", NS)
    if thumb is not None:
        url = thumb.get("url", "")
        if url:
            return url

    # محاولة استخراج أول صورة من الوصف
    match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', description or "", re.I)
    if match:
        return match.group(1)

    # محاولة enclosure
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

            # نخلي الملخص أطول، لكن بدون مبالغة
            if len(summary) > 700:
                summary = summary[:700].rs
