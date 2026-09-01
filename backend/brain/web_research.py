from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
from brain.gemini_client import get_gemini_response

def search_web(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)

        return [
            {
                "title" : r["title"],
                "url" : r["href"],
                "snippet" : r["body"]
            }
            for r in results
        ]

headers = {
    "User-Agent" : (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/136.0 Safari/537.36"
    )
}

def extract_content(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        for tag in soup(['script', 'style', 'noscript']):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        return text
    
    except requests.RequestException as e :
        return f"Error: {e}"

def research_topic(query):
    results = search_web(query)
    enriched = []
    for r in results:
        content = extract_content(r['url'])
        enriched.append({
            'title': r['title'],
            'url': r['url'],
            'snippet': r['snippet'],
            'content': content[:3000] if content and not content.startswith('Error') else r['snippet']
        })
    return enriched


LIVE_KEYWORDS = [
    "weather", "temperature", "forecast", "news", "latest", "current",
    "today", "stock", "price", "score", "live", "who won",
    "what happened", "right now", "trending", "update", "recently",
    "aqi", "air quality", "pollution", "humidity", "wind", "rain",
    "match", "result", "election", "breaking", "happening"
]

def needs_web_search(question):
    return any(word in question.lower() for word in LIVE_KEYWORDS)  
