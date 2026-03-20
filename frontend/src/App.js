import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  const [query, setQuery] = useState('India politics');
  const [pageSize, setPageSize] = useState(10);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/analyze`, {
        query: query,
        page_size: pageSize
      });

      if (response.data.success) {
        setResults(response.data);
      } else {
        setError('Analysis failed');
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to analyze news');
    } finally {
      setLoading(false);
    }
  };

  const getVerdictEmoji = (verdict) => {
    const emojiMap = {
      'LIKELY_REAL': '✅',
      'LIKELY_FAKE': '❌',
      'UNCERTAIN': '❓',
      'SATIRE': '😂'
    };
    return emojiMap[verdict] || '❓';
  };

  const getVerdictColor = (verdict) => {
    const colorMap = {
      'LIKELY_REAL': '#10b981',
      'LIKELY_FAKE': '#ef4444',
      'UNCERTAIN': '#f59e0b',
      'SATIRE': '#8b5cf6'
    };
    return colorMap[verdict] || '#6b7280';
  };

  const getCredibilityColor = (score) => {
    if (score >= 70) return '#10b981';
    if (score >= 40) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div className="App">
      <header className="header">
        <h1>🔍 Fake News Detection System</h1>
        <p>AI-powered analysis using multi-signal validation</p>
      </header>

      <div className="container">
        <div className="input-section">
          <div className="input-group">
            <label htmlFor="query">News Query:</label>
            <input
              id="query"
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., India politics"
            />
          </div>

          <div className="input-group">
            <label htmlFor="pageSize">Number of Articles:</label>
            <input
              id="pageSize"
              type="number"
              value={pageSize}
              onChange={(e) => setPageSize(Number(e.target.value))}
              min="1"
              max="20"
            />
          </div>

          <button 
            className="analyze-btn" 
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? 'Analyzing...' : 'Analyze News'}
          </button>
        </div>

        {error && (
          <div className="error-box">
            <strong>Error:</strong> {error}
          </div>
        )}

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Analyzing articles with AI models... This may take a minute.</p>
          </div>
        )}

        {results && results.summary && (
          <>
            <div className="summary-section">
              <h2>📊 Analysis Summary</h2>
              <div className="summary-grid">
                <div className="summary-card">
                  <div className="summary-value">{results.summary.analyzed_articles}</div>
                  <div className="summary-label">Articles Analyzed</div>
                </div>
                <div className="summary-card">
                  <div className="summary-value">{results.summary.average_credibility}%</div>
                  <div className="summary-label">Avg Credibility</div>
                </div>
                <div className="summary-card">
                  <div className="summary-value" style={{color: '#10b981'}}>
                    {results.summary.verdict_distribution.LIKELY_REAL}
                  </div>
                  <div className="summary-label">✅ Likely Real</div>
                </div>
                <div className="summary-card">
                  <div className="summary-value" style={{color: '#ef4444'}}>
                    {results.summary.verdict_distribution.LIKELY_FAKE}
                  </div>
                  <div className="summary-label">❌ Likely Fake</div>
                </div>
              </div>
            </div>

            <div className="results-section">
              <h2>📰 Detailed Analysis</h2>
              {results.results.map((item, idx) => (
                <div key={idx} className="article-card">
                  <div className="article-header">
                    <h3>
                      <span style={{color: getVerdictColor(item.validation.final_verdict)}}>
                        {getVerdictEmoji(item.validation.final_verdict)}
                      </span>
                      {' '}
                      {item.article.title}
                    </h3>
                    <span className="article-source">{item.article.source}</span>
                  </div>

                  <div className="verdict-section">
                    <div className="verdict-badge" style={{
                      backgroundColor: getVerdictColor(item.validation.final_verdict) + '20',
                      color: getVerdictColor(item.validation.final_verdict)
                    }}>
                      <strong>Verdict:</strong> {item.validation.final_verdict}
                    </div>
                    <div className="credibility-score">
                      <strong>Credibility:</strong>{' '}
                      <span style={{color: getCredibilityColor(item.validation.ensemble_score)}}>
                        {item.validation.ensemble_score.toFixed(1)}/100
                      </span>
                    </div>
                  </div>

                  <p className="article-summary">{item.analysis.summary}</p>

                  {item.analysis.reasons && item.analysis.reasons.length > 0 && (
                    <div className="analysis-section">
                      <h4>🔍 Analysis Indicators:</h4>
                      <ul>
                        {item.analysis.reasons.map((reason, i) => (
                          <li key={i}>{reason}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {item.analysis.red_flags && item.analysis.red_flags.length > 0 && (
                    <div className="analysis-section">
                      <h4>🚩 Red Flags:</h4>
                      <ul className="red-flags">
                        {item.analysis.red_flags.map((flag, i) => (
                          <li key={i}>{flag}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <div className="article-footer">
                    <a 
                      href={item.article.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="read-more"
                    >
                      Read Full Article →
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      <footer className="footer">
        <p>Powered by Groq LLMs (Llama 3.3 70B + Mixtral 8x7B)</p>
      </footer>
    </div>
  );
}

export default App;
