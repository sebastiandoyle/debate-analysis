# Presidential Debate Analysis

NLP sentiment analysis of US presidential debates across 60+ years of transcripts. Scrapes, parses, scores, and visualizes how candidates' language, tone, and aggression have shifted over decades.

## What It Does

- Downloads and parses presidential debate transcripts from public archives
- Runs sentiment analysis and keyword extraction on candidate responses
- Generates interactive visualizations of sentiment trends over time
- Includes focused analysis on specific policy topics (e.g., immigration)

## Key Findings

- Debate sentiment has trended progressively more negative since the 1960s
- Immigration-related language shows the sharpest polarization spike
- Candidates who speak more negatively about opponents tend to correlate with higher polling momentum (correlation, not causation)
- Response length has decreased over time — modern debates reward soundbites

## Tech Stack

- Python 3
- NLTK / TextBlob (sentiment scoring)
- scikit-learn (keyword extraction, topic modeling)
- Plotly / HTML (interactive visualizations)
- BeautifulSoup (transcript scraping)

## Usage

```bash
git clone https://github.com/sebastiandoyle/debate-analysis.git
cd debate-analysis
pip install -r requirements.txt

# Download transcripts
python3 download_debates.py

# Run analysis
python3 analyze.py

# View results
open visualization.html
```

## Files

```
debate-analysis/
├── download_debates.py          # Transcript scraper
├── analyze.py                   # Main NLP analysis pipeline
├── immigration_analysis.py      # Topic-specific deep dive
├── visualization.html           # Interactive results dashboard
├── transcripts/                 # Downloaded debate transcripts
└── results.json                 # Analysis output
```

## License

MIT
