import feedparser

RSS_URL = "https://www.jornada.com.mx/rss/cultura.xml?v=1"

feed = feedparser.parse(RSS_URL)

print("Feed:", feed.feed.get("title", "No title"))
print("Number of news items:", len(feed.entries))
print("-------------------------------------------------")

for entry in feed.entries:
    title = entry.get("title", "No title")
    content = entry.get("description", entry.get("summary", "No content"))

    print("TITLE:")
    print(title)

    print("\nCONTENT:")
    print(content)

    print("\n" + "-----------------------------------------------------")
