# 🔍 Fake News Detection System

AI-powered fake news detection with React frontend and Flask backend.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- NewsAPI key: https://newsapi.org/
- Groq API key: https://console.groq.com/

### 1. Setup Environment Variables

```bash
# Copy .env.example to .env and add your API keys
cp .env.example .env
```

Edit `.env`:
```
NEWSAPI_API_KEY=your_newsapi_key_here
GROQ_API_KEY=your_groq_key_here
```

### 2. Run Backend (Flask API)

**Option A - Automatic Setup (Recommended):**

Windows:
```bash
setup_backend.bat
```

Linux/Mac:
```bash
chmod +x setup_backend.sh
./setup_backend.sh
```

**Option B - Manual Setup:**

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
python app.py
```

Backend runs on `http://localhost:5000`

**Optional - CLI Version:**
```bash
# Make sure venv is activated
python main.py
```

### 3. Run Frontend (React)

Open a new terminal:

```bash
cd frontend
npm install
npm start
```

Frontend opens at `http://localhost:3000`

## 📋 Project Structure

```
news-analyzer/
├── backend/              # All backend code
│   ├── app.py           # Flask REST API
│   ├── main.py          # CLI version (optional)
│   ├── llm_analyzer.py  # Analysis engine
│   ├── llm_validator.py # Validation engine
│   ├── news_fetcher.py  # NewsAPI integration
│   ├── config.py        # Configuration
│   └── requirements.txt # Dependencies
└── frontend/            # React web interface
    ├── public/
    ├── src/
    └── package.json
```

## 🎯 Features

- Multi-signal validation (LLM + Source Credibility + Linguistics)
- Real-time analysis dashboard
- Verdict classification: LIKELY_FAKE, LIKELY_REAL, UNCERTAIN, SATIRE
- Credibility scoring (0-100)
- Beautiful responsive UI

## 🛠️ Tech Stack

**Backend**: Flask, Groq API (Llama 3.3 70B + Mixtral 8x7B), NewsAPI  
**Frontend**: React 18, Axios, CSS3
