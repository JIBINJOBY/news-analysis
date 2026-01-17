import os
import json
from dotenv import load_dotenv
from newsapi import NewsApiClient
from urllib.parse import urlparse

load_dotenv()

NEWS_API_KEY = os.getenv("NEWSAPI_API_KEY")

INDIAN_DOMAINS = [
    "thehindu.com",
    "timesofindia.indiatimes.com",
    "hindustantimes.com",
    "indianexpress.com",
    "ndtv.com",
    "indiatoday.in"
]

def fetch_news(query="India politics", page_size=15):
    if not NEWS_API_KEY:
        raise ValueError("NEWSAPI_API_KEY not found in .env")

    newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    response = newsapi.get_everything(
        q=query,
        language="en",
        sort_by="publishedAt",
        page_size=page_size,
    )

    articles = []

    for article in response.get("articles", []):
        if not article.get("content") or not article.get("url"):
            continue

        domain = urlparse(article["url"]).netloc

        if not any(indian_domain in domain for indian_domain in INDIAN_DOMAINS):
            continue

        articles.append({
            "title": article["title"],
            "source": article["source"]["name"],
            "url": article["url"],
            "content": article["content"]
        })

    return articles


def save_articles(articles, path="output/raw_articles.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2)


if __name__ == "__main__":
    articles = fetch_news()
    save_articles(articles)
    print(f"Saved {len(articles)} articles.")
