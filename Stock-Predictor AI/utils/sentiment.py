from textblob import TextBlob

def analyze_sentiments(news_items):
    sentiment_results = []

    for item in news_items:
        # Validate that item is a dictionary with title and url
        if isinstance(item, dict) and "title" in item and "url" in item:
            title = item["title"]
            url = item["url"]

            # Perform sentiment analysis on the title
            polarity = TextBlob(title).sentiment.polarity
            label = "POSITIVE" if polarity > 0 else "NEGATIVE" if polarity < 0 else "NEUTRAL"

            sentiment_results.append({
                "title": title,
                "url": url,
                "label": label,
                "score": round(abs(polarity), 2)
            })

    return sentiment_results
