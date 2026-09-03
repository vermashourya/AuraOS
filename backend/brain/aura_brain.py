import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime
from tracker.activity_tracker import get_running_apps, get_power_status, get_audio_status, get_hardware_status, get_network_status, get_security_status
from tracker.greeting import get_greeting
from brain.web_research import research_topic
from brain.gemini_client import get_gemini_response
from brain.response_parser import parse_aura_response, detect_response_type
import logging
import threading
import requests

PROXY_URL = "https://auraos-proxy.onrender.com"

def keep_proxy_alive():
    while True:
        try:
            requests.get(PROXY_URL, timeout=10)
        except Exception:
            pass
        threading.Event().wait(840)

threading.Thread(target=keep_proxy_alive, daemon=True).start()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def build_system_prompt():
    hardware = get_hardware_status()
    battery = get_power_status()
    network = get_network_status()
    running_apps = get_running_apps()
    greeting = get_greeting()
    time = datetime.now().strftime("%H:%M:%S")

    return f'''Current CPU usage is {hardware['CPU']['Usage']} and RAM usage is {hardware['RAM']['Usage']}.
    Current battery level is {battery['Percent']} and battery charging status is {battery['Plugged in']}.
    Connected to {network['Wi-Fi']['name']} with connectivity strength {network['Wi-Fi']['signal']}.
    Current time is {time} all currently running apps are{running_apps} and greeting message is {greeting}
    Start your response with exactly one of these tags: [TEXT], [WEATHER], [CODE], [DATA]. Then give your response.'''

def ask_aura(question, username='User'):
    try:
        context = build_system_prompt()
    except Exception:
        context = "System context not available"

    prompt = f'''Your name is Vision, an AI assistant embedded in AuraOS — inspired by the Vision supercomputer from Iron Man, created by Tony Stark.
    You are highly intelligent, calm, precise, and speak with a refined tone.
    The user's name is {username}. Use the user's name naturally, only when it feels appropriate — not in every response.
    System state: {context}
    User question: {question}
    Answer helpfully and concisely. Do NOT introduce yourself unless explicitly asked.'''

    try:
        response = get_gemini_response(prompt)
        formatted = parse_aura_response(response)
    except Exception as e:
        logging.error("ask_aura first attempt failed: %s", e)
        return {'type': 'text', 'content': 'Unavailable right now'}

    CANT_ANSWER_PHRASES = [
        "i don't have", "i do not have", "i cannot", "i can't",
        "no access", "real-time", "real time", "live data",
        "not able to", "unable to", "don't have access",
        "i'm sorry", "i am sorry", "as of my", "my knowledge",
        "i lack", "no information", "cannot provide"
    ]
    needs_web = any(p in formatted.lower() for p in CANT_ANSWER_PHRASES)

    if needs_web:
        web_context = ""
        try:
            results = research_topic(question)
            web_context = "\n\n".join(
                f"Source: {r['title']}\n{r['content'][:1000]}"
                for r in results
            )
        except Exception as e:
            logging.warning("web research failed: %s", e)

        if web_context:
            prompt = f'''Your name is Vision, an AI assistant embedded in AuraOS — inspired by the Vision supercomputer from Iron Man, created by Tony Stark.
    You are highly intelligent, calm, precise, and speak with a refined tone.
    The user's name is {username}. Use the user's name naturally, only when it feels appropriate — not in every response.
    System state: {context}
    Web research results (use this as your primary source): {web_context}
    User question: {question}
    Answer helpfully and concisely based on the web results. Do NOT introduce yourself unless explicitly asked.'''
            try:
                response = get_gemini_response(prompt)
                formatted = parse_aura_response(response)
            except Exception as e:
                logging.error("ask_aura web attempt failed: %s", e)

    try:
        response_type = detect_response_type(response)
    except Exception:
        response_type = 'text'

    return {'type': response_type, 'content': formatted}
