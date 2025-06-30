import os
import requests
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_company_news(ticker, max_articles=5):
    try:
        # Use a broader search query to increase chances of matching
        if '.' in ticker:
            company_name = ticker.split('.')[0]
        else:
            company_name = ticker
        
        # Add keywords to improve news hits
        query = f"{company_name} company OR {company_name} stock OR {company_name} share"

        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={query}&language=en&sortBy=publishedAt&pageSize={max_articles}&apiKey={"f361762608264f9fbb073170c5e90aa1"}"
        )

        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or "articles" not in data:
            raise Exception(data.get("message", "Unknown error occurred while fetching news."))

        articles = data["articles"]
        news_list = []

        for article in articles:
            news_item = {
                "title": article.get("title", "No title"),
                "url": article.get("url", "#"),
                "description": article.get("description", "No description available.")
            }
            news_list.append(news_item)

        return news_list if news_list else None

    except Exception as e:
        print("Error fetching news:", e)
        return None
