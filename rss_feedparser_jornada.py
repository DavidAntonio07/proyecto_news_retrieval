import feedparser
import csv
import uuid

RSS_URL = "https://www.jornada.com.mx/rss/cultura.xml?v=1"

feed = feedparser.parse(RSS_URL)

print("Feed:", feed.feed.get("title", "No title"))
print("Number of news items:", len(feed.entries))
print("-------------------------------------------------")

for entry in feed.entries:
    
    id = str(uuid.uuid1())  
    title = entry.get("title", "No title")
    content = entry.get("description", entry.get("summary", "No content"))
    url = entry.get("link", "No URL")
    date = entry.get("published", "No date")

    print("\nID:")
    print(id)
    
    print("\nTITLE:")
    print(title)

    print("\nCONTENT:")
    print(content)

    print("\nURL:")
    print(url)
    
    print("\nDATE:")
    print(date)
    
    
    
    print("\n" + "-----------------------------------------------------")
