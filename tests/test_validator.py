from news_fetcher import fetch_news
from llm_analyzer import analyze_article
from llm_validator import validate_analysis

articles = fetch_news()
analysis = analyze_article(articles[0])
validation = validate_analysis(articles[0], analysis)

print("Gemini Analysis:")
print(analysis)
print("\nMistral Validation:")
print(validation)
