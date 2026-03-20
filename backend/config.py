"""
Configuration file for Fake News Detection System
Centralized settings for all modules
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from parent directory (project root)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# ============= API KEYS =============
NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ============= MODEL SETTINGS =============
# Primary Analysis Model (Fast and powerful)
PRIMARY_MODEL = "llama-3.3-70b-versatile"

# Validation Model (Different model for diversity)
# Note: Mixtral-8x7b deprecated Feb 2026, using Llama 3.1 8B instead
VALIDATION_MODEL = "llama-3.1-8b-instant"

# Temperature settings
ANALYSIS_TEMPERATURE = 0.3  # Lower = more consistent
VALIDATION_TEMPERATURE = 0.2  # Even lower for validation

# ============= NEWS FETCHING =============
# Target domains for Indian news
INDIAN_DOMAINS = [
    "thehindu.com",
    "timesofindia.indiatimes.com",
    "hindustantimes.com",
    "indianexpress.com",
    "ndtv.com",
    "indiatoday.in",
    "thewire.in",
    "theprint.in",
    "scroll.in"
]

DEFAULT_QUERY = "India politics"
DEFAULT_PAGE_SIZE = 10

# ============= SOURCE CREDIBILITY TIERS =============
TIER1_SOURCES = [
    "The Hindu", "Indian Express", "The Indian Express",
    "PTI", "Press Trust of India", "ANI",
    "PIB", "Press Information Bureau"
]

TIER2_SOURCES = [
    "NDTV", "Times of India", "Hindustan Times",
    "India Today", "The Wire", "The Print", "Scroll"
]

TIER3_SOURCES = [
    "Mint", "Business Standard", "Economic Times",
    "Deccan Herald", "Deccan Chronicle"
]

# ============= SCORING THRESHOLDS =============
FAKE_THRESHOLD = 40  # Below this = LIKELY_FAKE
UNCERTAIN_THRESHOLD = 60  # Between 40-60 = UNCERTAIN
# Above 60 = LIKELY_REAL

HIGH_CONFIDENCE_THRESHOLD = 30  # Distance from 50
MEDIUM_CONFIDENCE_THRESHOLD = 15

# ============= OUTPUT SETTINGS =============
OUTPUT_DIR = "output"
ANALYSIS_JSON = f"{OUTPUT_DIR}/analysis_results.json"
FINAL_REPORT = f"{OUTPUT_DIR}/final_report.md"
RAW_ARTICLES = f"{OUTPUT_DIR}/raw_articles.json"

# ============= PROCESSING SETTINGS =============
REQUEST_DELAY = 1  # Seconds between requests (Groq is fast)
MAX_RETRIES = 3
TIMEOUT = 30  # Seconds

# ============= LAYER 2: RAG SETTINGS =============
# (Will be used in next layer)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_DB_PATH = "vector_db"
TOP_K_RESULTS = 5

# ============= LAYER 4: API SETTINGS =============
# (Will be used when building FastAPI)
API_HOST = "0.0.0.0"
API_PORT = 8000
CORS_ORIGINS = ["http://localhost:3000", "http://localhost:8000"]
