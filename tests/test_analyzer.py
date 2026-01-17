from news_fetcher import fetch_news
from llm_analyzer import analyze_article

articles = fetch_news()
print(analyze_article(articles[0]))
