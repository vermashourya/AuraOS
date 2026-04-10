# This will act as a bridge between python and react

import pythoncom
from greeting import get_greeting
from fastapi import FastAPI
from activity_tracker import get_power_status , get_network_status , get_hardware_status , get_audio_status , get_security_status , get_running_apps

app = FastAPI()

@app.get('/')
def home():
    return {'message':'Aura OS API is running'}

@app.get('/battery')
def battery():
    return get_power_status()

@app.get('/network')
def network():
    return get_network_status()

@app.get('/hardware')
def hardware():
    pythoncom.CoInitialize()
    return get_hardware_status()

@app.get("/audio")
def audio():
    return get_audio_status()

@app.get("/security")
def security():
    pythoncom.CoInitialize()
    return get_security_status()

@app.get('/apps')
def apps():
    pythoncom.CoInitialize()
    running = get_running_apps()
    return {'apps':list(running)}

@app.get('/greeting')
def greet():
    pythoncom.CoInitialize()
    return {'message':get_greeting()}