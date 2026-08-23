import winreg
import sys
import os

REGISTRY_KEY = r'Software\Microsoft\Windows\CurrentVersion\Run'
APP_NAME = 'AuraOS' 

def get_startup_command():
    pythonw = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
    main_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tracker', 'main.py')
    return f'"{pythonw}" "{main_py}" '

def enable_startup():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, get_startup_command())
    winreg.CloseKey(key)

def disable_startup():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)
    except FileNotFoundError:
        pass

def is_startup_enabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, winreg.KEY_READ)
        winreg.QueryValueEx(key, APP_NAME)
        winreg.CloseKey(key)
        return True 
    except FileNotFoundError:
        return False