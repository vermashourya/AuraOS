import threading
import sys
import os

if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    
    WRITE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    WRITE_DIR = BASE_DIR

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
    from tracker.main import start_aura, take_snapshot, stop_aura
    import time
    session_id = start_aura()
    try:
        while True:
            take_snapshot(session_id)
            time.sleep(300)
    except Exception:
        stop_aura(session_id)

def start_tray():
    import time
    time.sleep(2) # Give API time to start
    from tray import start_tray_thread
    start_tray_thread()

def start_api():
    import uvicorn
    uvicorn.run('api:app', host='127.0.0.1', port=8000, log_config=UVICORN_LOG_CONFIG)

if __name__ == '__main__':
    # Start tracker daemon
    threading.Thread(target=start_tracker, daemon=True).start()

    # Start tray daemon separately so a crash in tracker doesn't kill tray
    threading.Thread(target=start_tray, daemon=True).start()

    # Keep main thread for API
    start_api()
