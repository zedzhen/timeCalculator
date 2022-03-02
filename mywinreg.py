import winreg
from constant import NAME

REG_PATH = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
ACCESS = winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE

def add(path):
    w=winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, access=ACCESS)
                 
    winreg.SetValueEx(w, NAME, None, winreg.REG_SZ, f'"{path}" -auto')
                 
    winreg.CloseKey(w)

def rem():
    w=winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, access=ACCESS)

    try:
        winreg.DeleteValue(w, NAME)
    except FileNotFoundError:
        pass

    winreg.CloseKey(w)
