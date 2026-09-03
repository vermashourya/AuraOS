import whisper
import tempfile
import os
import asyncio
import edge_tts
import ctypes
import time
import threading

model = whisper.load_model('base')

def _run_transcribe(tmp_path: str, result_container: dict):
    try:
        result = model.transcribe(tmp_path)
        result_container['text'] = result['text'].strip()
    except Exception as e:
        result_container['error'] = str(e)

def transcribe(audio_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        f.write(audio_bytes)
        tmp_path = f.name
    try:
        result_container = {}
        t = threading.Thread(target=_run_transcribe, args=(tmp_path, result_container))
        t.start()
        t.join()
        if 'error' in result_container:
            raise Exception(result_container['error'])
        return result_container.get('text', '')
    finally:
        os.unlink(tmp_path)

stop_event = threading.Event()

async def speak_async(text: str):
    stop_event.clear()
    communicate = edge_tts.Communicate(text, voice='en-GB-RyanNeural')
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        tmp_path = f.name
    try:
        await communicate.save(tmp_path)
        winmm = ctypes.windll.winmm
        winmm.mciSendStringW(f'open "{tmp_path}" type mpegvideo alias mp3', None, 0, None)
        winmm.mciSendStringW('play mp3', None, 0, None)
        buf = ctypes.create_unicode_buffer(128)
        while not stop_event.is_set():
            winmm.mciSendStringW('status mp3 mode', buf, 128, None)
            if buf.value != 'playing':
                break
            time.sleep(0.2)
        winmm.mciSendStringW('stop mp3', None, 0, None)
        winmm.mciSendStringW('close mp3', None, 0, None)
    finally:
        os.unlink(tmp_path)

def speak(text: str):
    asyncio.run(speak_async(text))

def stop_speaking():
    stop_event.set()
