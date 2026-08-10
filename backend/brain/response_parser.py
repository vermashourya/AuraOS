import json
import re
import html

def detect_response_type(response):
    text = response.text.strip()

    code_pattern = [
        r"```[\s\S]*```",          
        r"\bdef\s+\w+\(",
        r"\bclass\s+\w+",
        r"#include\s*<",
        r"console\.log\(",
        r"public\s+static\s+void",
        r"SELECT\s+.+\s+FROM",
        r"function\s+\w+\(",
    ]
    if any(re.search(p, text, re.IGNORECASE) for p in code_pattern):
        return "code"
    
    weather = [
        "temperature",
        "humidity",
        "forecast",
        "rain",
        "wind speed",
        "weather",
        "°c",
        "°f",
        "sunny",
        "cloudy",
    ]
    if any(word in text.lower() for word in weather):
        return "weather"
    
    data_patterns = [
        r"\$\d+", 
        r"\brows?\b", 
        r"\bcolumns?\b", 
        r"\btable\b", 
        r"\bjson\b"
    ]

    number_ratio = len(re.findall(r"\d", text)) / max(len(text), 1)
    if number_ratio > 0.3 or any(re.search(p, text, re.IGNORECASE) for p in data_patterns):
        return "data"
    
    return "text"

def format_response(response, response_type):
    text = response.text.strip()

    if response_type == "weather":
        return f"🌤 WEATHER REPORT\n\n{(text)}"

    return text
    
def parse_aura_response(raw_reponse):
    response_type = detect_response_type(raw_reponse)
    formatted_response = format_response(raw_reponse, response_type)
    
    return formatted_response