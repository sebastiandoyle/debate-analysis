import requests
import re
import json
from bs4 import BeautifulSoup
import time

BASE = "https://www.debates.org"
transcripts = []

# Get list of transcript URLs
print("Fetching transcript list...")
resp = requests.get(f"{BASE}/voter-education/debate-transcripts/")
soup = BeautifulSoup(resp.text, 'html.parser')

links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if 'debate-transcript' in href and href != '/voter-education/debate-transcripts/':
        links.append(href)

links = list(set(links))
print(f"Found {len(links)} transcripts")

# Download each transcript
for i, link in enumerate(links[:30]):  # Limit to 30 for speed
    url = BASE + link if link.startswith('/') else link
    print(f"Downloading {i+1}/{len(links[:30])}: {link[:50]}...")
    
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Extract text content
        content = soup.get_text(separator=' ')
        content = re.sub(r'\s+', ' ', content)
        
        # Try to extract year from URL or content
        year_match = re.search(r'(19[6-9]\d|20[0-2]\d)', link)
        year = year_match.group(1) if year_match else "unknown"
        
        transcripts.append({
            'url': link,
            'year': year,
            'text': content,
            'length': len(content)
        })
        time.sleep(0.5)
    except Exception as e:
        print(f"  Error: {e}")

# Save to JSON
with open('debates.json', 'w') as f:
    json.dump(transcripts, f)

print(f"\nSaved {len(transcripts)} transcripts to debates.json")
