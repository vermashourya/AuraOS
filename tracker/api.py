# This will act as a bridge between python and react

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pythoncom
from greeting import get_greeting
from activity_tracker import get_power_status , get_network_status , get_hardware_status , get_audio_status , get_security_status , get_running_apps

app = FastAPI()

app.add_middleware(
    CORSMiddleware , allow_origins = ["*"] , allow_methods = ["*"] , allow_headers = ["*"]
)

@app.get('/')
def home():
    return {'message':'Aura OS API is running'}

# This will send the battery info to the dashboard
@app.get('/battery')
def battery():
    return get_power_status()

# This will send the network info to the dashboard
@app.get('/network')
def network():
    return get_network_status()

# This will send the hardware info to the dashboard
@app.get('/hardware')
def hardware():
    pythoncom.CoInitialize()
    return get_hardware_status()

# This will send the audio info to the dashboard
@app.get("/audio")
def audio():
    pythoncom.CoInitialize()
    return get_audio_status()

# This will send the security info to the dashboard
@app.get("/security")
def security():
    pythoncom.CoInitialize()
    return get_security_status()

# This will send the running apps info to the dashboard
@app.get('/apps')
def apps():
    pythoncom.CoInitialize()
    running = get_running_apps()
    return {'apps':list(running)}

# This will send the greeting message to the dashboard
@app.get('/greeting')
def greet():
    pythoncom.CoInitialize()
    return {'message':get_greeting()}