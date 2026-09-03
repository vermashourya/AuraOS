# Single entry point for AuraOS — starts tracker + API server
import threading
import sys
import os

# Redirect None streams when frozen with --noconsole
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

# When frozen by PyInstaller, files are extracted to sys._MEIPASS
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    # exe lives one level above _MEIPASS — use that for writable files (logs, db)
    WRITE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    WRITE_DIR = BASE_DIR

# Add BASE_DIR to path so api.py and all modules are importable
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.makedirs(os.path.join(WRITE_DIR, 'logs'), exist_ok=True)
LOG_FILE = os.path.join(WRITE_DIR, 'logs', 'uvicorn.log')

UVICORN_LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()': 'logging.Formatter',
            'fmt': '%(asctime)s %(levelname)s %(message)s',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'default',
        },
    },
    'loggers': {
        'uvicorn':        {'handlers': ['file'], 'level': 'INFO', 'propagate': False},
        'uvicorn.error':  {'handlers': ['file'], 'level': 'INFO', 'propagate': False},
        'uvicorn.access': {'handlers': ['file'], 'level': 'INFO', 'propagate': False},
    },
}

def start_tracker():
    # Import and run tracker directly — subprocess won't work when frozen
    # since sys.executable is the .exe, not python.exe
    from tracker.main import start_aura, take_snapshot, stop_aura, start_tray_thread
    import time
    session_id = start_aura()
    start_tray_thread()
    try:
        while True:
            take_snapshot(session_id)
            time.sleep(300)
    except Exception:
        stop_aura(session_id)

def start_api():
    import uvicorn
    uvicorn.run('api:app', host='127.0.0.1', port=8000, log_config=UVICORN_LOG_CONFIG)

if __name__ == '__main__':
    threading.Thread(target=start_tracker, daemon=True).start()
    start_api()
