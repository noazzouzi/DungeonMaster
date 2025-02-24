import win32gui
import win32con
import pygetwindow
import time

def window(display):
    # Récupérer le handle de la fenêtre Dofus
    hwnd = win32gui.FindWindow(None, display)  # Mets ici le nom exact de la fenêtre

    if hwnd:
        #win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restaure la fenêtre si réduite
        win32gui.SetForegroundWindow(hwnd)  # Met la fenêtre au premier plan
        time.sleep(1)  # Laisse le temps à la fenêtre d'être active