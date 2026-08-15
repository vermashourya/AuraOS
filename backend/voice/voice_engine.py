import whisper
import tempfile
import os
import asyncio
import edge_tts
import ctypes
import time

model = whisper.load_model('base')
speaking = False

def transcribe(audio_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f :
        f.write(audio_bytes)
        tmp_path = f.name
    try:
        result = model.transcribe(tmp_path)
        return result['text'].strip()
    finally:
        os.unlink(tmp_path)

async def speak_async(text: str):
    global speaking
    speaking = True
    communicate = edge_tts.Communicate(text, voice='en-US-AriaNeural')
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        tmp_path = f.name
    try:
        await communicate.save(tmp_path)
        winmm = ctypes.windll.winmm
        winmm.mciSendStringW(f'open "{tmp_path}" type mpegvideo alias mp3', None, 0 , None)
        winmm.mciSendStringW('play mp3 wait', None, 0 , None)
        winmm.mciSendStringW('close mp3', None, 0 , None)
        buf = ctypes.create_unicode_buffer(128)
        while speaking:
            winmm.mciSendStringW('status mp3 mode', buf, 128, None)
            if buf.value != 'playing':
                break 
            time.sleep(0.2)
        winmm.mciSendStringW('stop mp3', None, 0, None)
        winmm.mciSendStringW('close mp3', None, 0, None)
    finally:
        speaking = False
        os.unlink(tmp_path)

def speak(text: str):
    asyncio.run(speak_async(text))

def stop_speaking():
    global speaking
    speaking = False