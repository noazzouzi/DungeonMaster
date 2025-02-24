import os
import time
import psutil
import pyautogui
import pygetwindow as gw

# Étape 1 : Fermer tous les processus Dofus
def kill_game():
    processes = ["Dofus", "something"]
    for process in psutil.process_iter(['pid', 'name']):
        for p in processes:
            if p in process.info['name']:
                try:
                    os.kill(process.info['pid'], 9)
                    print(f"Processus " + str(p) + " fermé : PID {process.info['pid']}")
                except Exception as e:
                    print(f"Erreur en fermant " + p + " : {e}")