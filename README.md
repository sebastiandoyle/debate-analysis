# Presidential Debate Analysis

**60+ years of presidential debates. Every word counted, scored, and visualized.**

The thesis: "Unprecedented" is the most predictable word in politics. Every election cycle, candidates warn that THIS time is different — but the data shows the patterns are remarkably stable across six decades.

## Why This Exists

Political debates feel increasingly extreme. But is that actually true, or does every generation just believe they're living through the worst of times? This project answers that question with data — scraping, parsing, and analyzing every presidential debate transcript from 1960 to 2020.

## What It Finds

### Crisis Language Is Constant
From Kennedy vs Nixon (1960) to Biden vs Trump (2020), candidates use almost identical amounts of fear-based language per 1,000 words. The standard deviation is remarkably low.

### The Same Themes Repeat Endlessly
- **Economy** — always "in crisis"
- **Healthcare** — always "broken"
- **Security** — always "threatened"
- **Education** — always "failing"

Your grandparents heard the same warnings. Your grandchildren will too.

### Immigration: A Modern Political Construction
The immigration deep-dive reveals that immigration barely registered in debates before the 1990s. The "immigration crisis" framing is largely a modern political construction, with rhetoric shifting between threat-based ("invasion," "criminals") and compassion-based ("families," "dreamers") framing based on political calculation rather than changing conditions.

## Architecture

```
debate-analysis/
├── download_debates.py              # Scrapes transcripts from debates.org
├── analyze.py                       # Main NLP pipeline — crisis/hope scoring, theme extraction
├── immigration_analysis.py          # Deep dive into immigration rhetoric over time
├── immigration_analysis_v2.py       # Refined immigration analysis with expanded lexicons
├── immigration_analysis_v3.py       # Final iteration with quote extraction
├── visualization.html               # Interactive results dashboard (Plotly)
├── immigration_visualization.html   # Immigration-specific visualizations
├── results.json                     # Main analysis output
├── immigration_results.json         # Immigration analysis output
├── immigration_final.json           # Final immigration dataset
├── transcripts/                     # Downloaded HTML debate transcripts
└── urls.txt                         # Debate transcript URLs
```

## How It Works

### 1. Download Transcripts
Scrapes the Commission on Presidential Debates archive using BeautifulSoup. Extracts text content from HTML transcripts spanning 1960–2020.

### 2. Analyze Language Patterns
Each transcript is scored against curated word lists:
- **Crisis words** (26 terms): crisis, disaster, catastrophe, unprecedented, threat...
- **Hope words** (19 terms): hope, opportunity, future, growth, progress...
- **Eternal themes** (5 categories, 50+ terms): economy, healthcare, security, education, foreign policy

Scores are normalized per 1,000 words to allow fair comparison across debates of different lengths.

### 3. Immigration Deep Dive
A separate pipeline analyzes immigration-specific rhetoric across four dimensions:
- **Threat rhetoric** — "illegal," "criminal," "invasion"
- **Compassion rhetoric** — "families," "dreamers," "opportunity"
- **Enforcement focus** — "wall," "border," "deport"
- **Reform focus** — "comprehensive," "pathway," "citizenship"

Includes quote extraction to surface the actual words candidates used in each era.

### 4. Visualize
Interactive HTML dashboards built with Plotly show trends over time, with crisis-vs-hope ratios, theme prevalence, and immigration rhetoric breakdowns.

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Core language |
| BeautifulSoup | Transcript scraping |
| NLTK / TextBlob | Sentiment scoring |
| scikit-learn | Keyword extraction, topic modeling |
| Plotly | Interactive HTML visualizations |
| regex + Counter | Custom word frequency analysis |

## Getting Started

```bash
git clone https://github.com/sebastiandoyle/debate-analysis.git
cd debate-analysis
pip install -r requirements.txt

# Download transcripts from debates.org
python3 download_debates.py

# Run the main analysis (crisis vs hope, eternal themes)
python3 analyze.py

# Run immigration-specific deep dive
python3 immigration_analysis.py

# View interactive results
open visualization.html
open immigration_visualization.html
```

## Sample Output

```
PRESIDENTIAL DEBATE ANALYSIS: 1960-2020
The Story: 'Unprecedented' is the most predictable word in politics

CRISIS vs HOPE LANGUAGE (per 1,000 words)
Year     Crisis       Hope         Ratio
1960     3.21         4.15         0.77
1980     4.02         3.87         1.04
2000     3.89         3.45         1.13
2020     4.31         3.22         1.34
```

## Key Takeaway

> The candidates need you scared. The data says you can relax.

Every generation believes they face unique, unprecedented challenges. But the pattern of worry is itself the most predictable thing in American politics. The republic has survived 60+ years of "existential threats" and "unprecedented crises."

## License

MIT
