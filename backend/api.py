from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pythoncom
from tracker.greeting import get_greeting
from tracker.activity_tracker import get_power_status , get_network_status , get_hardware_status , get_audio_status , get_security_status , get_running_apps
from tracker.productivity_engine import get_productivity_report
from tracker.prediction_engine import get_predictions
from brain.aura_brain import ask_aura
from brain.web_research import research_topic
from pydantic import BaseModel
import json
from pathlib import Path
from voice.voice_engine import transcribe, speak, stop_speaking
import threading
from startup import enable_startup, disable_startup, is_startup_enabled
from logger import logger

app = FastAPI()

app.add_middleware(
    CORSMiddleware , allow_origins = ["*"] , allow_methods = ["*"] , allow_headers = ["*"]
)

@app.get('/')
def home():
    return {'message':'Aura OS API is running'}


@app.get('/battery')
def battery():
    try:
        return get_power_status()
    except Exception as e :
        logger.error(f'/hardware failed: {e}')
        return {'error' : str(e)}


@app.get('/network')
def network():
    try:
        return get_network_status()
    except Exception as e :
        return {'error' : str(e)}


@app.get('/hardware')
def hardware():
    try:
        pythoncom.CoInitialize()
        return get_hardware_status()
    except Exception as e :
        return {'error' : str(e)}


@app.get("/audio")
def audio():
    try:
        pythoncom.CoInitialize()
        return get_audio_status()
    except Exception as e :
        return {'error' : str(e)}


@app.get("/security")
def security():
    try:
        pythoncom.CoInitialize()
        return get_security_status()
    except Exception as e :
        return {'error' : str(e)}


@app.get('/apps')
def apps():
    try:
        pythoncom.CoInitialize()
        running = get_running_apps()
        return {'apps':list(running)}
    except Exception as e :
        return {'error' : str(e)}


@app.get('/greeting')
def greet():
    try:
        pythoncom.CoInitialize()
        return {'message':get_greeting()}
    except Exception as e :
        return {'error' : str(e)}


@app.get('/productivity')
def report():
    try:
        return get_productivity_report()
    except Exception as e :
        return {'error' : str(e)}


@app.get('/predictions')
def prediction():
    try:
        pythoncom.CoInitialize()
        return get_predictions()
    except Exception as e :
        return {'error' : str(e)}

class Question(BaseModel):
    question : str

@app.post('/ask')
async def ask(request : Question):
    try:
        pythoncom.CoInitialize()
        response = ask_aura(request.question)
    except Exception as e :
        logger.error(f'/ask failed: {e}')
        return {'error' : str(e)}

    return response

class Research(BaseModel):
    query : str

@app.post('/research')
async def research(request : Research):
    try:
        pythoncom.CoInitialize()
        result = research_topic(request.query)
        return{
                "query" : request.query,
                "result" : result
            }
    except Exception as e :
        return {'error' : str(e)}

HISTORY_FILE = Path(__file__).parent / 'conversations.json'

class Messages(BaseModel):
    messages: list

@app.get('/history')
def get_history():
    try:
        if not HISTORY_FILE.exists():
            return {'messages': []}
        with open (HISTORY_FILE, 'r') as f :
            return json.load(f)
    except Exception as e :
        return {'error' : str(e)}
    
@app.post('/history/save')
def save_history(request : Messages):
    try:
        with open (HISTORY_FILE, 'w') as f :
            json.dump({'messages': request.messages}, f)
        return {'status': 'saved'}
    except Exception as e :
        return {'error' : str(e)}


@app.post('/voice/input')
async def voice_input(audio: UploadFile = File(...)):
    try:
        audio_bytes = await audio.read()
        transcript = transcribe(audio_bytes)
        return {'transcript': transcript}
    except Exception as e :
        logger.error(f'/voice/input failed: {e}')
        return {'error' : str(e)}

@app.post('/voice/speak')
async def voice_speak(request: Question):
    try:
        threading.Thread(target=speak, args=(request.question,), daemon=True).start()
        return {'status':'speaking'}
    except Exception as e :
        return {'error' : str(e)}

@app.post('/voice/stop')
def voice_stop():
    try:
        stop_speaking()
        return {'status': 'stopped'}
    except Exception as e :
        return {'error' : str(e)}

@app.get('/startup')
def get_startup():
    try:
        return {'enabled': is_startup_enabled()}
    except Exception as e:
        return {'error': str(e)}

@app.post('/startup')
def set_startup(request: Question):
    try:
        if request.question == 'enable':
            enable_startup()
        else:
            disable_startup()
        return {'enabled': is_startup_enabled()}
    except Exception as e:
        return {'error': str(e)}
