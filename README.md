# Presidential Debate Analysis

NLP sentiment analysis of US presidential debates across 60+ years of transcripts.

## What It Does

- Downloads and parses presidential debate transcripts from public archives
- Runs sentiment analysis and keyword extraction on candidate responses
- Generates interactive visualizations of sentiment trends over time
- Includes focused analysis on specific policy topics (e.g., immigration)

## Tech Stack

- **Python 3** - Core analysis pipeline
- **NLP** - Sentiment scoring, keyword extraction, topic modeling
- **HTML/JS** - Interactive data visualizations

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

## Usage

```bash
# Download transcripts
python3 download_debates.py

# Run analysis
python3 analyze.py

# View results
open visualization.html
```
