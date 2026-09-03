import threading
import subprocess
import sys
import os
from PIL import Image, ImageDraw
import pystray

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def create_icon_image():
    icon_path = os.path.join(get_base_dir(), 'icon.png')
    if os.path.exists(icon_path):
        return Image.open(icon_path).convert('RGBA')
    # Fallback: create a simple solid color icon if file missing
    img = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((4, 4, 60, 60), fill='#4ade80')
    return img

def open_dashboard(icon, item):
    import subprocess
    try:
        # Try to find and activate the Vision window
        subprocess.run(['powershell', '-Command',
                       '(New-Object -ComObject WScript.Shell).AppActivate("Vision")'],
                      capture_output=True)
    except:
        pass

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
