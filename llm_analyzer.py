import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=GEMINI_API_KEY)

ALLOWED_SENTIMENTS = ["positive", "negative", "neutral"]
ALLOWED_TONES = ["analytical", "urgent", "balanced", "satirical"]

def analyze_article(article):
    prompt = f"""
You are a news analyst.

Analyze the following Indian political news article and return:
1. Gist (1–2 sentences)
2. Sentiment: one of {ALLOWED_SENTIMENTS}
3. Tone: one of {ALLOWED_TONES}

Article Title:
{article['title']}

Article Content:
{article['content']}

Respond ONLY in valid JSON like:
{{
  "gist": "...",
  "sentiment": "...",
  "tone": "..."
}}
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text.strip()
