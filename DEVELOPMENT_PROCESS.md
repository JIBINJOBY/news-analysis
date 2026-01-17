# Development Process – News Analysis with Dual LLM Validation

## Overview

The goal of this assignment was to build a small but realistic AI pipeline that mimics how LLMs can be used in real-world analysis and validation workflows. I chose **Option A (News Analysis with Dual LLM Validation)** because it closely resembles production use cases such as content moderation, fact-checking support, and automated news analysis.

The system follows a clear pipeline:

**Fetch news → Analyze with LLM #1 → Validate with LLM #2 → Save structured output**

I focused on clean modular design, clear responsibilities per file, and realistic handling of API limitations.

---

## Project Structure & Design Decisions

I structured the project using small, single-responsibility modules:

- `news_fetcher.py` handles only data ingestion
- `llm_analyzer.py` performs primary semantic analysis
- `llm_validator.py` performs independent validation
- `main.py` orchestrates the full pipeline and output generation

This separation made it easier to test and debug each component independently before combining them.

A Python virtual environment was used to isolate dependencies and ensure reproducibility.

---

## News Data Collection

I used **NewsAPI** to fetch recent Indian political news.  
Initially, I observed that NewsAPI returns international articles that reference India, so I refined the pipeline by filtering articles based on **Indian news domains** (e.g., Indian Express, The Hindu, NDTV).

This helped reduce noise while still keeping enough articles (8–12) for analysis.

I avoided overly aggressive filtering (such as strict per-source limits) to ensure sufficient data volume for the LLM analysis stage.

---

## LLM #1: Primary Analysis (Gemini)

For the first stage of analysis, I used **Google Gemini**.

### Why Gemini?
- Strong summarization capabilities
- Good performance on sentiment and tone classification
- Free-tier access suitable for take-home assignments
- Easy integration via Python SDK

I initially faced issues due to deprecated Gemini SDKs and model identifiers. After investigating available models, I migrated to the **Gemini 3 preview models** and selected:

**`gemini-3-flash-preview`**

This model is optimized for fast text analysis and works well for structured outputs.

Each article is analyzed for:
- A short gist (1–2 sentences)
- Sentiment (positive / negative / neutral)
- Tone (analytical / urgent / balanced / satirical)

The prompt enforces **strict JSON output** to ensure downstream compatibility.

---

## LLM #2: Validation (Mistral via OpenRouter)

To reduce single-model bias, I introduced a second LLM to validate the first model’s output.

### Why Mistral via OpenRouter?
- Independent model family (reduces confirmation bias)
- Strong reasoning despite smaller size
- Free-tier availability
- Simple REST-based integration

LLM #2 does **not** perform real-world fact checking.  
Instead, it validates whether Gemini’s analysis is **logically consistent with the article text**.

In other words, it checks:
- Does the gist reflect the article?
- Is the sentiment justified by the language used?
- Is the tone classification reasonable?
- Did the first model hallucinate anything?

This mirrors real-world cross-model validation patterns commonly used in AI systems.

---

## Orchestration & Batch Processing

The `main.py` file orchestrates the full pipeline:

1. Fetch articles
2. Analyze each article using Gemini
3. Validate the analysis using Mistral
4. Save structured results to `analysis_results.json`
5. Generate a human-readable `final_report.md`

Each article is processed independently, and failures are handled gracefully. If an article fails due to an API error, the pipeline skips it and continues.

---

## Handling API Rate Limits

While processing articles, I encountered **Gemini free-tier rate limits (5 requests/minute)**.  
Instead of failing the pipeline, errors were caught and logged, and the system continued processing remaining articles.

In a production system, this could be improved by:
- Adding retry logic with exponential backoff
- Introducing request throttling or queue-based processing
- Using batch or async workflows

For the scope of this assignment, graceful degradation was sufficient and intentional.

---

## Testing Approach

Testing was done incrementally:
- Individual components (news fetching, single-article analysis, validation) were tested in isolation
- Integration was tested using a small batch of articles
- Output formats were manually verified for correctness and readability

This incremental approach helped catch issues early and simplified debugging.

---

## Limitations & Future Improvements

- LLM validation is logic-based, not factual verification
- No external retrieval or search is used
- Rate limits slow down batch processing

With more time, I would:
- Add retrieval-based fact checking (RAG)
- Introduce async processing
- Add more robust automated tests
- Store results in a database for larger-scale analysis

---

## Final Notes

This project was built with a focus on **clarity, robustness, and real-world AI engineering practices**, rather than maximizing model complexity. The dual-LLM approach demonstrates how multiple models can work together to improve reliability, even within free-tier constraints.
