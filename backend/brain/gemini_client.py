import requests

PROXY_URL = "https://auraos-proxy.onrender.com/gemini"

class ProxyResponse:
    def __init__(self, text):
        self.text = text

def get_gemini_response(prompt):
    response = requests.post(PROXY_URL, json={"prompt": prompt}, timeout=60)
    data = response.json()
    if "error" in data:
        raise Exception(data["error"])
    return ProxyResponse(data["text"])
