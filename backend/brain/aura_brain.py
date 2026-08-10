# This will going to be the brain of AuraOS

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime
from tracker.activity_tracker import get_running_apps, get_power_status, get_audio_status, get_hardware_status, get_network_status, get_security_status
from tracker.greeting import get_greeting
from brain.web_research import needs_web_search, research_topic
from brain.context_engine import build_full_context
from brain.gemini_client import get_gemini_response
from brain.response_parser import parse_aura_response, detect_response_type
import logging

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
    Current time is {time} all currently running apps are{running_apps} and greeting message is {greeting}'''

def ask_aura(question):
    try: 
        context = build_system_prompt() 
    except Exception:
        context = "System context not available"

    try:   
        need_web_search = needs_web_search(question)
    except Exception:
        need_web_search = False

    web_context = ""
    if need_web_search:
        try:
            results = research_topic(question)
            web_context = "\n\n".join(
                f"Source: {r['title']}\n{r['snippet']}\n{r['content'][:1000]}"
                for r in results
            )
        except Exception as e:
            logging.warning("build_full_context falied : %s", e)

    prompt = f'''You are Aura, an AI assistant embedded in AuraOS.
    System state: {context}
    {"Web research results (use this as your primary source): " + web_context if web_context else ""}
    User question: {question}
    Answer helpfully and concisely based on the web results if available. Do NOT introduce yourself unless explicitly asked.'''

    try:
        response = get_gemini_response(prompt)
        response_type = detect_response_type(response)
        formatted = parse_aura_response(response)
        return {'type': response_type, 'content': formatted}
    except Exception as e :
        logging.error("ask_aura failed: %s", e)
        return {'type': 'text', 'content': 'Unavailable right now'}