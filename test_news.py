from news import get_stock_news
from sentiment import analyze_sentiment


symbol = "AAPL"

news_items = get_stock_news(symbol)

for item in news_items:
    title = item["title"]
    sentiment = analyze_sentiment(title)

    print("\nTitle:", title)
    print("Publisher:", item["publisher"])
    print("Sentiment:", sentiment["label"])
    print("Score:", sentiment["score"])
    print("Link:", item["link"])