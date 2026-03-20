import json
import datetime
import time
from news_fetcher import fetch_news
from llm_analyzer import analyze_article
from llm_validator import validate_analysis


OUTPUT_JSON = "output/analysis_results.json"
OUTPUT_MD = "output/final_report.md"


def generate_markdown_report(results):
    """
    Generate comprehensive fake news detection report.
    """
    date = datetime.date.today().isoformat()

    # Count verdicts
    verdict_count = {
        "LIKELY_FAKE": 0,
        "LIKELY_REAL": 0,
        "UNCERTAIN": 0,
        "SATIRE": 0
    }
    
    avg_credibility = 0
    high_risk_articles = []

    for item in results:
        analysis = item["analysis"]
        validation = item["validation"]
        
        verdict = validation.get("final_verdict", "UNCERTAIN")
        if verdict in verdict_count:
            verdict_count[verdict] += 1
        
        ensemble_score = validation.get("ensemble_score", 50)
        avg_credibility += ensemble_score
        
        if ensemble_score < 40:
            high_risk_articles.append((item, ensemble_score))
    
    if results:
        avg_credibility /= len(results)

    lines = []
    lines.append("# 🔍 Fake News Detection Report\n\n")
    lines.append(f"**Date:** {date}\n")
    lines.append(f"**Articles Analyzed:** {len(results)}\n")
    lines.append(f"**Average Credibility Score:** {avg_credibility:.1f}/100\n")
    lines.append("**Detection System:** Groq LLM (Llama 3.3 70B + Mixtral 8x7B)\n\n")

    lines.append("## 📊 Verdict Distribution\n\n")
    lines.append(f"- ✅ **LIKELY REAL:** {verdict_count['LIKELY_REAL']} articles\n")
    lines.append(f"- ❌ **LIKELY FAKE:** {verdict_count['LIKELY_FAKE']} articles\n")
    lines.append(f"- ❓ **UNCERTAIN:** {verdict_count['UNCERTAIN']} articles\n")
    lines.append(f"- 😂 **SATIRE:** {verdict_count['SATIRE']} articles\n\n")
    
    if high_risk_articles:
        lines.append("## ⚠️ High Risk Articles (Credibility < 40)\n\n")
        for item, score in sorted(high_risk_articles, key=lambda x: x[1]):
            article = item["article"]
            lines.append(f"- **[{article['title']}]({article['url']})** - Score: {score:.1f}\n")
        lines.append("\n")

    lines.append("## 📰 Detailed Analysis\n\n")

    for idx, item in enumerate(results, start=1):
        article = item["article"]
        analysis = item["analysis"]
        validation = item["validation"]
        
        verdict = validation.get("final_verdict", "UNCERTAIN")
        ensemble_score = validation.get("ensemble_score", 50)
        confidence = validation.get("confidence_level", "MEDIUM")
        
        verdict_emoji = {
            "LIKELY_REAL": "✅",
            "LIKELY_FAKE": "❌",
            "UNCERTAIN": "❓",
            "SATIRE": "😂"
        }.get(verdict, "❓")

        lines.append(f"### {verdict_emoji} Article {idx}: {article['title']}\n\n")
        lines.append(f"**Source:** {article['source']}  \n")
        lines.append(f"**URL:** [{article['url']}]({article['url']})  \n\n")
        
        lines.append(f"**🎯 Verdict:** {verdict}  \n")
        lines.append(f"**📊 Ensemble Credibility Score:** {ensemble_score:.1f}/100  \n")
        lines.append(f"**🔒 Confidence Level:** {confidence}  \n\n")
        
        lines.append(f"**📝 Summary:** {analysis.get('summary', 'N/A')}  \n\n")
        
        # Primary analysis reasons
        reasons = analysis.get('reasons', [])
        if reasons:
            lines.append("**🔍 Analysis Indicators:**\n")
            for reason in reasons:
                lines.append(f"- {reason}\n")
            lines.append("\n")
        
        # Red flags
        red_flags = analysis.get('red_flags', [])
        if red_flags:
            lines.append("**🚩 Red Flags:**\n")
            for flag in red_flags:
                lines.append(f"- {flag}\n")
            lines.append("\n")
        
        # Claims verification
        claims = analysis.get('verified_claims', [])
        if claims:
            lines.append("**✔️ Fact-Checked Claims:**\n")
            for claim in claims:
                status_emoji = {
                    "VERIFIED": "✅",
                    "UNVERIFIED": "❓",
                    "CONTRADICTED": "❌",
                    "PARTIALLY_TRUE": "⚠️"
                }.get(claim.get('status', 'UNVERIFIED'), "❓")
                lines.append(f"{status_emoji} *{claim.get('claim', 'N/A')}*  \n")
                if claim.get('evidence'):
                    lines.append(f"   Evidence: {claim['evidence']}  \n")
            lines.append("\n")
        
        # Source credibility
        source_cred = validation.get('source_credibility', {})
        lines.append(f"**📰 Source Reputation:** {source_cred.get('tier', 'Unknown')} (Score: {source_cred.get('score', 0)}/100)  \n\n")
        
        # LLM validation
        llm_val = validation.get('llm_validation', {})
        if llm_val.get('disagreements'):
            lines.append("**⚖️ Validator Notes:**\n")
            for disagreement in llm_val['disagreements']:
                lines.append(f"- {disagreement}\n")
            lines.append("\n")
        
        lines.append("---\n\n")

    return "".join(lines)


def main():
    print("\n" + "="*60)
    print("🔍 FAKE NEWS DETECTION SYSTEM")
    print("="*60)
    print("Layer 1: Core Detection with Groq API")
    print("="*60 + "\n")
    
    print("📡 Fetching Indian political news articles...")
    articles = fetch_news(query="India politics", page_size=10)
    
    if not articles:
        print("❌ No articles fetched. Check your NewsAPI key.")
        return
    
    print(f"✅ Found {len(articles)} articles\n")

    results = []
    start_time = time.time()

    for idx, article in enumerate(articles, start=1):
        print(f"\n[{idx}/{len(articles)}] Processing: {article['title'][:60]}...")

        try:
            # Primary fake news analysis (Groq Llama 3.3)
            print("  🔎 Analyzing with Llama 3.3...")
            analysis_text = analyze_article(article)
            analysis_json = json.loads(analysis_text)
            print(f"     ➜ Verdict: {analysis_json.get('verdict')} (Score: {analysis_json.get('credibility_score')})")

            # Multi-signal validation (Mixtral + heuristics)
            print("  🔐 Validating with ensemble signals...")
            validation = validate_analysis(article, analysis_text)
            print(f"     ➜ Final Score: {validation['ensemble_score']:.1f}/100 ({validation['final_verdict']})")

            results.append({
                "article": article,
                "analysis": analysis_json,
                "validation": validation
            })
            
            # Small delay to avoid rate limits (Groq is fast, minimal delay needed)
            time.sleep(1)

        except Exception as e:
            print(f"  ❌ Error: {e}")
            continue

    elapsed = time.time() - start_time
    
    if not results:
        print("\n❌ No articles successfully analyzed.")
        return

    # Save JSON output
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Save Markdown report
    markdown = generate_markdown_report(results)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(markdown)

    print("\n" + "="*60)
    print("✅ FAKE NEWS DETECTION COMPLETED")
    print("="*60)
    print(f"📊 Analyzed: {len(results)}/{len(articles)} articles")
    print(f"⏱️  Time: {elapsed:.1f}s ({elapsed/len(results):.1f}s per article)")
    print(f"💾 Results saved:")
    print(f"   - JSON: {OUTPUT_JSON}")
    print(f"   - Report: {OUTPUT_MD}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
