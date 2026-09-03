import threading
import subprocess
import sys
import os
from PIL import Image
import pystray

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def create_icon_image():
    return Image.open(os.path.join(get_base_dir(), 'icon.png')).convert('RGBA')

def open_dashboard(icon, item):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    dashboard_dir = os.path.join(BASE_DIR, '..', 'dashboard')
    subprocess.Popen(
        ['npm', 'run', 'electron'],
        cwd=os.path.normpath(dashboard_dir),
        shell=True
    )

def quit_aura(icon, item):
    icon.stop()
    os._exit(0)

def build_menu():
    return pystray.Menu(
        pystray.MenuItem('Open Dashboard', open_dashboard, default=True),
        pystray.MenuItem('Quit Vision', quit_aura)
    )

def run_tray():
    icon = pystray.Icon(
        name='Vision',
        icon=create_icon_image(),
        title='Vision',
        menu=build_menu()
    )
    icon.run()

def start_tray_thread():
    t = threading.Thread(target=run_tray, daemon=True)
    t.start()
