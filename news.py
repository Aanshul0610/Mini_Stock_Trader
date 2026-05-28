import yfinance as yf


# Fetch latest stock news from yfinance
def get_stock_news(symbol, limit=5):
    stock = yf.Ticker(symbol)
    news_items = stock.news

    results = []

    for item in news_items[:limit]:
        content = item.get("content", {})

        title = content.get("title", "No title available")

        publisher_info = content.get("provider", {})
        publisher = publisher_info.get("displayName", "Unknown publisher")

        link_info = content.get("canonicalUrl", {})
        link = link_info.get("url", "")

        results.append({
            "title": title,
            "publisher": publisher,
            "link": link
        })

    return results