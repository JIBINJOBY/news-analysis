import os
import json
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path

# Load .env from parent directory (project root)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=GROQ_API_KEY)

# Model: Fast and powerful for analysis
MODEL = "llama-3.3-70b-versatile"

VERDICTS = ["LIKELY_FAKE", "LIKELY_REAL", "UNCERTAIN", "SATIRE"]
CLAIM_STATUSES = ["VERIFIED", "UNVERIFIED", "CONTRADICTED", "PARTIALLY_TRUE"]

def analyze_article(article):
    """
    Analyze article for fake news detection with credibility scoring.
    Returns structured JSON with verdict, credibility score, and extracted claims.
    """
    prompt = f"""
You are an expert fake news detection system analyzing Indian political news.

Analyze the following article for credibility and potential misinformation:

Title: {article['title']}
Source: {article['source']}
Content: {article['content']}

Perform a comprehensive fake news analysis and return ONLY valid JSON:

{{
  "verdict": "LIKELY_FAKE" or "LIKELY_REAL" or "UNCERTAIN" or "SATIRE",
  "credibility_score": 0-100,
  "confidence": 0.0-1.0,
  "summary": "Brief 1-2 sentence summary of the article",
  "reasons": [
    "List specific red flags or credibility indicators",
    "E.g., 'No primary source cited', 'Headline exaggerates claim', 'Verifiable facts present'"
  ],
  "verified_claims": [
    {{
      "claim": "Specific factual claim made in the article",
      "status": "VERIFIED" or "UNVERIFIED" or "CONTRADICTED" or "PARTIALLY_TRUE",
      "evidence": "Brief explanation or null if no evidence"
    }}
  ],
  "red_flags": [
    "Emotional language",
    "Anonymous sources",
    "Clickbait headline",
    "Missing context",
    "Outdated information"
  ],
  "source_credibility": {{
    "known_outlet": true/false,
    "reputation_score": 0-100,
    "notes": "Brief assessment of source reliability"
  }}
}}

Be analytical and objective. Focus on factual indicators of misinformation.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert fact-checker specializing in detecting misinformation in Indian political news. You analyze articles critically and provide structured, evidence-based assessments."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent analysis
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error analyzing article: {e}")
        # Return a safe fallback
        return json.dumps({
            "verdict": "UNCERTAIN",
            "credibility_score": 50,
            "confidence": 0.0,
            "summary": "Analysis failed",
            "reasons": [f"Error: {str(e)}"],
            "verified_claims": [],
            "red_flags": [],
            "source_credibility": {
                "known_outlet": False,
                "reputation_score": 0,
                "notes": "Analysis error"
            }
        })
