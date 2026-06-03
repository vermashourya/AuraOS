import json
import re
from brain.aura_brain import get_gemini_response

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
    
    data_pattern = [
        r"\b\d+(\.\d+)?%",
        r"\b\d{4}\b",
        r"\$\d+",
        r"\brows?\b",
        r"\bcolumns?\b",
        r"\btable\b",
        r"\bjson\b",
    ]
    number_ratio = len(re.findall(r"\d", text)) / max(len(text), 1)
    if number_ratio > 0.15 or any(re.search(p, text, re.IGNORECASE) for p in data_pattern):
        return "data"
    
    return "text"

def format_response(response , response_type):
    text = response.text.strip()

    if response_type == "code":
        if"'''" in text :
            return text 
        
        return f"'''{text}'''"
    
    elif response_type == "data":
        try:
            parse = json.loads(text)
            format = []

            for key, value in parse.items():
                format.append(f"{key}:{value}")
            
            return "\n".join(format)
        
        except: pass

        pairs = []
        lines = text.splitlines()
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                pairs.append(f"{key.strip()}:{value.strip()}")
        
        if pairs:
            return "\n".join(pairs)
        
        return text
    
    elif response_type == "weather":
        return f"🌤 WEATHER REPORT\n\n{text}"
    
    else: 
        return text
    
def parse_aura_response(raw_reponse):
    response_type = detect_response_type(raw_reponse)
    formatted_response = format_response(raw_reponse, response_type)
    
    return formatted_response