from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import datetime
import time

from news_fetcher import fetch_news
from llm_analyzer import analyze_article
from llm_validator import validate_analysis

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Store analysis results in memory (in production, use a database)
latest_results = []


@app.route('/', methods=['GET'])
def home():
    """Root endpoint with API information"""
    return jsonify({
        'message': '🔍 Fake News Detection API',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'analyze': '/api/analyze (POST)',
            'results': '/api/results',
            'article': '/api/analyze/<id>'
        },
        'frontend': 'http://localhost:3000'
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Fake News Detection API is running'})


@app.route('/api/analyze', methods=['POST'])
def analyze_news():
    """
    Analyze news articles for fake news detection
    Request body: { "query": "India politics", "page_size": 10 }
    """
    try:
        data = request.get_json()
        query = data.get('query', 'India politics')
        page_size = data.get('page_size', 10)
        
        # Fetch articles
        articles = fetch_news(query=query, page_size=page_size)
        
        if not articles:
            return jsonify({'error': 'No articles fetched. Check your NewsAPI key.'}), 400
        
        results = []
        errors = []
        
        print(f"📰 Fetched {len(articles)} articles")
        
        for idx, article in enumerate(articles, 1):
            try:
                print(f"[{idx}/{len(articles)}] Analyzing: {article.get('title', 'No title')[:60]}...")
                
                # Primary analysis
                analysis_text = analyze_article(article)
                analysis_json = json.loads(analysis_text)
                
                # Validation
                validation = validate_analysis(article, analysis_text)
                
                results.append({
                    "article": article,
                    "analysis": analysis_json,
                    "validation": validation
                })
                
                print(f"✅ Success: {validation.get('final_verdict')}")
                
                # Small delay to avoid rate limits
                time.sleep(1)
                
            except Exception as e:
                error_msg = f"Article {idx}: {str(e)}"
                print(f"❌ Error: {error_msg}")
                errors.append(error_msg)
                continue
        
        # Store latest results
        global latest_results
        latest_results = results
        
        # Calculate summary statistics
        verdict_count = {
            "LIKELY_FAKE": 0,
            "LIKELY_REAL": 0,
            "UNCERTAIN": 0,
            "SATIRE": 0
        }
        
        avg_credibility = 0
        for item in results:
            validation = item["validation"]
            verdict = validation.get("final_verdict", "UNCERTAIN")
            if verdict in verdict_count:
                verdict_count[verdict] += 1
            avg_credibility += validation.get("ensemble_score", 50)
        
        if results:
            avg_credibility /= len(results)
        
        return jsonify({
            'success': True,
            'summary': {
                'total_articles': len(articles),
                'analyzed_articles': len(results),
                'failed_articles': len(errors),
                'verdict_distribution': verdict_count,
                'average_credibility': round(avg_credibility, 1)
            },
            'results': results,
            'errors': errors if errors else None
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze/<int:article_id>', methods=['GET'])
def get_article_analysis(article_id):
    """Get analysis for a specific article by index"""
    if article_id < 0 or article_id >= len(latest_results):
        return jsonify({'error': 'Article not found'}), 404
    
    return jsonify(latest_results[article_id])


@app.route('/api/results', methods=['GET'])
def get_latest_results():
    """Get the latest analysis results"""
    return jsonify({
        'total': len(latest_results),
        'results': latest_results
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔍 FAKE NEWS DETECTION API")
    print("="*60)
    print("Starting Flask server on http://localhost:5000")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
