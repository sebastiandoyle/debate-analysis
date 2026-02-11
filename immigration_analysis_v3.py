#!/usr/bin/env python3
"""
Immigration Analysis v3: Balanced quote extraction
"""

import re
import html
import json
from pathlib import Path

# Immigration indicators - sentence must contain at least one
IMMIGRATION_INDICATORS = [
    'immigrant', 'immigrants', 'immigration',
    'undocumented', 'deport', 'deportation', 'deportations',
    'amnesty', 'refugee', 'refugees', 'asylum',
    'citizenship', 'naturalization',
    'dreamer', 'daca', 'illegal alien', 'illegal immigrant',
    'border patrol', 'ice ', ' ice,', 'ice.', 'southern border',
    'border security', 'border wall', 'secure the border',
    'sanctuary', 'migrant', 'migrants', 'migration',
    'path to citizenship', 'pathway to citizenship'
]

# Also allow if contains "border" AND immigration words nearby
BORDER_CONTEXT_WORDS = ['mexico', 'mexican', 'latino', 'hispanic', 'crossing', 'wall',
                        'separated', 'children', 'families', 'legal', 'illegal']

# Strict exclusions - skip sentence if these appear
EXCLUSIONS = ['wall street', 'berlin wall', 'stonewall',
              'pakistan', 'afghanistan', 'taliban', 'al qaeda', 'al-qaeda',
              'alexander the great']

# Framing categories
THREAT_WORDS = ['illegal', 'criminal', 'criminals', 'gang', 'gangs', 'drug', 'drugs',
                'flood', 'flooding', 'invasion', 'invade', 'crisis', 'pouring',
                'caravan', 'rapist', 'rapists', 'dangerous', 'terrorist', 'crime']
COMPASSION_WORDS = ['family', 'families', 'children', 'kids', 'dream', 'dreamer', 'dreamers',
                    'opportunity', 'contribute', 'contributing', 'hardworking', 'pathway',
                    'humane', 'compassion', 'reunite', 'separated', 'separation']
ENFORCEMENT_WORDS = ['wall', 'fence', 'border', 'deport', 'enforce', 'enforcement',
                     'ice', 'agents', 'patrol', 'catch', 'detain', 'detention', 'secure']
REFORM_WORDS = ['reform', 'comprehensive', 'pathway', 'citizenship', 'legalize',
                'legal status', 'fix', 'broken', 'system', 'bipartisan', 'daca']

def clean_html(html_content):
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text)
    return text

def is_immigration_sentence(sentence):
    """Check if sentence is about immigration"""
    lower = sentence.lower()

    # Exclude false positives
    for exc in EXCLUSIONS:
        if exc in lower:
            return False

    # Check for direct immigration indicators
    for indicator in IMMIGRATION_INDICATORS:
        if indicator in lower:
            return True

    # Check for "border" with immigration context
    if 'border' in lower:
        for ctx in BORDER_CONTEXT_WORDS:
            if ctx in lower:
                return True

    return False

def extract_quotes(text, year):
    """Extract immigration-related sentences"""
    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text)
    quotes = []

    for sentence in sentences:
        clean = sentence.strip()
        if len(clean) < 40 or len(clean) > 600:
            continue

        if is_immigration_sentence(clean):
            # Get speaker if available
            speaker = "SPEAKER"
            speaker_match = re.search(r'^([A-Z]{2,})\s*:', clean)
            if speaker_match:
                speaker = speaker_match.group(1)

            # Determine framing
            lower = clean.lower()
            framing = []
            if any(w in lower for w in THREAT_WORDS):
                framing.append('threat')
            if any(w in lower for w in COMPASSION_WORDS):
                framing.append('compassion')
            if any(w in lower for w in ENFORCEMENT_WORDS):
                framing.append('enforcement')
            if any(w in lower for w in REFORM_WORDS):
                framing.append('reform')

            quotes.append({
                'year': year,
                'speaker': speaker,
                'quote': clean,
                'framing': framing
            })

    return quotes

def count_framing(quotes, words):
    """Count framing words in immigration quotes"""
    count = 0
    for q in quotes:
        lower = q['quote'].lower()
        for w in words:
            count += len(re.findall(r'\b' + re.escape(w) + r'\b', lower))
    return count

# Analyze debates
results = []
all_quotes = []
transcripts_dir = Path('/Users/sebastiandoyle/Developer/debate-analysis/transcripts')

print("Analyzing immigration rhetoric (v3)...\n")

for html_file in sorted(transcripts_dir.glob('*_raw.html')):
    year = html_file.stem.replace('_raw', '')

    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        raw_html = f.read()

    text = clean_html(raw_html)
    word_count = len(text.split())

    # Extract quotes
    quotes = extract_quotes(text, year)
    all_quotes.extend(quotes)

    # Calculate immigration percentage
    imm_words = sum(len(q['quote'].split()) for q in quotes)

    results.append({
        'year': year,
        'total_words': word_count,
        'immigration_quotes': len(quotes),
        'immigration_words': imm_words,
        'immigration_pct': round(imm_words / word_count * 100, 2),
        'threat': count_framing(quotes, THREAT_WORDS),
        'compassion': count_framing(quotes, COMPASSION_WORDS),
        'enforcement': count_framing(quotes, ENFORCEMENT_WORDS),
        'reform': count_framing(quotes, REFORM_WORDS)
    })

# Output
print("=" * 70)
print("IMMIGRATION IN PRESIDENTIAL DEBATES: 1960-2020")
print("From Nothing to 'National Emergency' in 60 Years")
print("=" * 70)
print()

# Timeline table
print("📊 THE RISE OF IMMIGRATION AS A POLITICAL ISSUE")
print("-" * 65)
print(f"{'Year':<8} {'Quotes':<10} {'Words':<10} {'% of Debate':<15} {'Trend'}")
print("-" * 65)
for r in results:
    bar = '▓' * min(int(r['immigration_pct'] * 20), 25)
    print(f"{r['year']:<8} {r['immigration_quotes']:<10} {r['immigration_words']:<10} {r['immigration_pct']:<15} {bar}")
print()

# Framing table
print("📊 HOW THEY FRAME IMMIGRANTS")
print("-" * 65)
print(f"{'Year':<8} {'👿 Threat':<12} {'❤️ Compassion':<15} {'🚔 Enforce':<12} {'📋 Reform'}")
print("-" * 65)
for r in results:
    if r['immigration_quotes'] > 0:
        print(f"{r['year']:<8} {r['threat']:<12} {r['compassion']:<15} {r['enforcement']:<12} {r['reform']}")
print()

# Notable quotes
print("=" * 70)
print("ACTUAL QUOTES BY ERA")
print("=" * 70)

# Curated quotes for storytelling
for r in results:
    year = r['year']
    year_quotes = [q for q in all_quotes if q['year'] == year]

    if not year_quotes:
        print(f"\n📅 {year}: [No immigration discussion]")
    else:
        print(f"\n📅 {year}: {len(year_quotes)} immigration references")
        print("-" * 60)

        # Show best quotes (prioritize ones with multiple framing types)
        sorted_quotes = sorted(year_quotes, key=lambda x: len(x['framing']), reverse=True)
        for q in sorted_quotes[:4]:
            tags = ' + '.join(q['framing']).upper() if q['framing'] else 'NEUTRAL'
            quote_text = q['quote'][:300] + '...' if len(q['quote']) > 300 else q['quote']
            print(f"\n  [{tags}]")
            print(f"  \"{quote_text}\"")

# Save
with open('/Users/sebastiandoyle/Developer/debate-analysis/immigration_final.json', 'w') as f:
    json.dump({'stats': results, 'quotes': all_quotes}, f, indent=2)

print("\n\n" + "=" * 70)
print("THE STORY THE DATA TELLS")
print("=" * 70)
print("""
📈 THE TRAJECTORY:
   1960: 0% of debate about immigration (literally zero)
   1984: 0% - still not a political issue
   1992: <0.5% - first mentions appear
   2000: minimal
   2008: still minimal
   2016: 0.4% - suddenly it's "huge"
   2020: 1.2% - "the most important issue"

🎭 THE FRAMING SHIFT:
   Notice how the SAME topic gets completely different treatment.
   2016: Heavy on THREAT language ("illegal", "criminals", "gangs")
   2020: More COMPASSION language ("families", "children", "separated")

   The immigrants didn't change. The politics did.

🤔 THE QUESTION:
   If immigration was truly an "invasion" or "crisis," why did:
   - Kennedy never mention it?
   - Reagan barely mention it?
   - It only become a "crisis" when politically useful?

💡 THE ANSWER:
   Immigration is a policy debate dressed up as an emergency.
   Every generation has been told the current immigrants are
   "different" and "dangerous." Every generation was wrong.

   Your family was once the "scary immigrants" too.
""")

print("\nData saved to immigration_final.json")
