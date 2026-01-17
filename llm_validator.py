import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL_NAME = "mistralai/mistral-7b-instruct"

def validate_analysis(article, analysis_json):
    prompt = f"""
You are a fact-checking assistant.

Given the original news article and an LLM-generated analysis, verify whether the analysis is correct.

Article Title:
{article['title']}

Article Content:
{article['content']}

LLM Analysis:
{analysis_json}

Respond in JSON format only:
{{
  "is_correct": true/false,
  "issues": "Describe any errors or say 'No issues found'"
}}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"].strip()
