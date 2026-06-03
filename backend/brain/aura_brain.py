# This will going to be the brain of AuraOS

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime
from tracker.activity_tracker import get_running_apps, get_power_status, get_audio_status, get_hardware_status, get_network_status, get_security_status
from tracker.greeting import get_greeting
from brain.web_research import needs_web_search
from brain.context_engine import build_full_context
from brain.gemini_client import get_gemini_response

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
    context = build_system_prompt()    

    need_web_search = needs_web_search(question)

    if need_web_search:
        context = build_full_context()

    prompt = f'''Your name is Aura and you are an AI assistant.
    Here is the current system state :{context},
    User question :{question},
    Answer helpfully and personally.'''

    return get_gemini_response(prompt).text