import win32gui
import win32con
import pygetwindow
import time

def window(characterName):
    # Récupérer le handle de la fenêtre Dofus
    characterWindow = find_window_by_text(characterName)
    print("character window : " + str(characterWindow))
    hwnd = characterWindow[0]  # Mets ici le nom exact de la fenêtre

    if hwnd:
        #win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restaure la fenêtre si réduite
        win32gui.SetForegroundWindow(hwnd)  # Met la fenêtre au premier plan
        time.sleep(1)  # Laisse le temps à la fenêtre d'être active

def find_window_by_text(target_text):
    def enum_window_callback(hwnd, lParam):
        # Obtenir le titre de la fenêtre
        window_title = win32gui.GetWindowText(hwnd)

        # Vérifier si le texte cible est dans le titre de la fenêtre
        if target_text.lower() in window_title.lower():
            # Si trouvé, ajouter cette fenêtre à la liste des fenêtres correspondantes
            print(f"Fenêtre trouvée : {window_title}")
            windows_found.append(hwnd)
    
    windows_found = []

    # Enumérer toutes les fenêtres ouvertes
    win32gui.EnumWindows(enum_window_callback, None)
    
    return windows_found