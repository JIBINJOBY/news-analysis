import json
import datetime
import time
from news_fetcher import fetch_news
from llm_analyzer import analyze_article
from llm_validator import validate_analysis


OUTPUT_JSON = "output/analysis_results.json"
OUTPUT_MD = "output/final_report.md"


def generate_markdown_report(results):
    date = datetime.date.today().isoformat()

    sentiment_count = {"positive": 0, "negative": 0, "neutral": 0}

    for item in results:
        sentiment = item["analysis"].get("sentiment", "neutral")
        if sentiment in sentiment_count:
            sentiment_count[sentiment] += 1

    lines = []
    lines.append("# News Analysis Report\n")
    lines.append(f"**Date:** {date}\n")
    lines.append(f"**Articles Analyzed:** {len(results)}\n")
    lines.append("**Source:** NewsAPI\n\n")

    lines.append("## Summary\n")
    lines.append(f"- Positive: {sentiment_count['positive']} articles\n")
    lines.append(f"- Negative: {sentiment_count['negative']} articles\n")
    lines.append(f"- Neutral: {sentiment_count['neutral']} articles\n\n")

    lines.append("## Detailed Analysis\n")

    for idx, item in enumerate(results, start=1):
        article = item["article"]
        analysis = item["analysis"]
        validation = item["validation"]

        lines.append(f"### Article {idx}: \"{article['title']}\"\n")
        lines.append(f"- **Source:** {article['source']}\n")
        lines.append(f"- **Link:** {article['url']}\n")
        lines.append(f"- **Gist:** {analysis.get('gist')}\n")
        lines.append(f"- **LLM#1 Sentiment:** {analysis.get('sentiment')}\n")
        lines.append(f"- **Tone:** {analysis.get('tone')}\n")
        lines.append(f"- **LLM#2 Validation:** {validation}\n\n")

    return "".join(lines)


def main():
    print("Fetching news articles...")
    articles = fetch_news()

    results = []

    for idx, article in enumerate(articles, start=1):
        print(f"Processing article {idx}/{len(articles)}")

        try:
            analysis_text = analyze_article(article)
            analysis_json = json.loads(analysis_text)

            validation_text = validate_analysis(article, analysis_text)

            results.append({
                "article": article,
                "analysis": analysis_json,
                "validation": validation_text
            })
            time.sleep(15)

        except Exception as e:
            print(f"Skipping article due to error: {e}")

    # Save JSON output
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Save Markdown report
    markdown = generate_markdown_report(results)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(markdown)

    print("\n✅ Pipeline completed successfully.")
    print(f"Saved {len(results)} articles.")
    print(f"- JSON: {OUTPUT_JSON}")
    print(f"- Report: {OUTPUT_MD}")


if __name__ == "__main__":
    main()
