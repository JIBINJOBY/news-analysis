import os
import json
import re
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

# Use a different model for validation (model diversity)
# Updated: Mixtral deprecated, using Llama 3.1 8B for fast validation
VALIDATION_MODEL = "llama-3.1-8b-instant"

def calculate_source_credibility(source_name):
    """
    Calculate credibility score based on known source reputation.
    Layer 3: Multi-signal validation component.
    """
    # Tier 1: Highly trusted Indian news outlets
    tier1_sources = [
        "The Hindu", "Indian Express", "The Indian Express",
        "PTI", "Press Trust of India", "ANI",
        "PIB", "Press Information Bureau"
    ]
    
    # Tier 2: Mainstream outlets
    tier2_sources = [
        "NDTV", "Times of India", "Hindustan Times",
        "India Today", "The Wire", "The Print"
    ]
    
    # Tier 3: Regional/smaller outlets
    tier3_sources = [
        "Mint", "Business Standard", "Economic Times",
        "Deccan Herald", "Deccan Chronicle"
    ]
    
    source_lower = source_name.lower()
    
    for source in tier1_sources:
        if source.lower() in source_lower:
            return {"score": 90, "tier": "Tier 1 - Highly Trusted"}
    
    for source in tier2_sources:
        if source.lower() in source_lower:
            return {"score": 75, "tier": "Tier 2 - Mainstream"}
    
    for source in tier3_sources:
        if source.lower() in source_lower:
            return {"score": 65, "tier": "Tier 3 - Regional"}
    
    return {"score": 40, "tier": "Unknown Source"}

def detect_linguistic_red_flags(article):
    """
    Detect linguistic deception signals.
    Layer 3: Multi-signal validation component.
    """
    title = article.get('title', '').lower()
    content = article.get('content', '').lower()
    
    red_flags = []
    deception_score = 0
    
    # Clickbait patterns
    clickbait_patterns = [
        r'you won\'t believe',
        r'shocking',
        r'amazing',
        r'this one trick',
        r'doctors hate',
        r'breaking:.*!+',
        r'\bwow\b'
    ]
    
    for pattern in clickbait_patterns:
        if re.search(pattern, title):
            red_flags.append("Clickbait headline pattern detected")
            deception_score += 15
            break
    
    # Excessive punctuation
    if title.count('!') > 1 or title.count('?') > 1:
        red_flags.append("Excessive punctuation in headline")
        deception_score += 10
    
    # All caps words (excluding common acronyms)
    caps_words = re.findall(r'\b[A-Z]{4,}\b', title)
    if len(caps_words) > 2:
        red_flags.append("Excessive capitalization for emphasis")
        deception_score += 10
    
    # Emotional manipulation keywords
    emotional_keywords = [
        'outrage', 'fury', 'slammed', 'blasted', 'destroyed',
        'annihilated', 'crushed', 'demolished', 'ripped apart'
    ]
    
    emotional_count = sum(1 for keyword in emotional_keywords if keyword in title or keyword in content[:200])
    if emotional_count >= 2:
        red_flags.append("Emotionally charged language")
        deception_score += 10
    
    # Anonymous sources warning
    if 'sources said' in content or 'anonymous source' in content:
        red_flags.append("Reliance on anonymous sources")
        deception_score += 5
    
    return {
        "red_flags": red_flags,
        "deception_score": min(deception_score, 50),  # Cap at 50
        "linguistic_confidence": max(0, 100 - deception_score) / 100
    }

def validate_analysis(article, analysis_json):
    """
    Multi-signal validation combining:
    1. LLM cross-validation
    2. Source credibility
    3. Linguistic deception signals
    
    Returns ensemble score instead of simple agree/disagree.
    """
    try:
        analysis = json.loads(analysis_json)
    except:
        analysis = {"verdict": "UNCERTAIN", "credibility_score": 50}
    
    # Signal 1: LLM Cross-Validation
    prompt = f"""
You are a fact-checking validator. Review this fake news analysis for logical consistency.

Article Title: {article['title']}
Article Content: {article['content']}

Primary Analysis:
{analysis_json}

Validate:
1. Does the verdict match the evidence presented?
2. Are the red flags accurate?
3. Is the credibility score reasonable?
4. Are there any logical contradictions?

Respond ONLY in valid JSON:
{{
  "validation_verdict": "AGREES" or "DISAGREES" or "PARTIAL",
  "confidence": 0.0-1.0,
  "disagreements": ["List any logical issues or contradictions"],
  "suggested_score_adjustment": -20 to +20,
  "reasoning": "Brief explanation"
}}
"""
    
    try:
        response = client.chat.completions.create(
            model=VALIDATION_MODEL,
            messages=[
                {"role": "system", "content": "You are a critical fact-checking validator who identifies logical inconsistencies and biases in fake news detection."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        llm_validation = json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Validation LLM error: {e}")
        llm_validation = {
            "validation_verdict": "UNCERTAIN",
            "confidence": 0.5,
            "disagreements": [],
            "suggested_score_adjustment": 0,
            "reasoning": "Validation failed"
        }
    
    # Signal 2: Source Credibility
    source_cred = calculate_source_credibility(article.get('source', ''))
    
    # Signal 3: Linguistic Red Flags
    linguistic = detect_linguistic_red_flags(article)
    
    # Ensemble Scoring
    base_score = analysis.get('credibility_score', 50)
    adjustment = llm_validation.get('suggested_score_adjustment', 0)
    source_weight = source_cred['score'] * 0.3  # 30% weight
    linguistic_weight = linguistic['linguistic_confidence'] * 100 * 0.2  # 20% weight
    
    final_score = (
        base_score * 0.5 +  # 50% weight to primary analysis
        source_weight +
        linguistic_weight +
        adjustment
    )
    final_score = max(0, min(100, final_score))  # Clamp to 0-100
    
    return {
        "ensemble_score": round(final_score, 2),
        "original_score": base_score,
        "llm_validation": llm_validation,
        "source_credibility": source_cred,
        "linguistic_analysis": linguistic,
        "final_verdict": "LIKELY_FAKE" if final_score < 40 else "UNCERTAIN" if final_score < 60 else "LIKELY_REAL",
        "confidence_level": "HIGH" if abs(final_score - 50) > 30 else "MEDIUM" if abs(final_score - 50) > 15 else "LOW"
    }
