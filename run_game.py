import time
import subprocess
import pyautogui
import window
import json

with open("config/config.json", "r", encoding="utf-8") as file:
    config = json.load(file)
display = config["app_name"]

def run_game():
    launcher_path = r"C:\Users\nouam\OneDrive\Documents\Ankama\something.exe"
    subprocess.Popen(launcher_path, cwd=r"C:\Users\nouam\OneDrive\Documents\Ankama")
    print("Launcher lancé.")
    time.sleep(5)  # Attendre que le launcher s'ouvre

    window.window(display)

    # Étape 3 : Sélectionner les comptes et cliquer sur "Connecter"
    pyautogui.moveTo(1250, 550)  # Ajuste ces coordonnées selon l'endroit de la liste des comptes
    time.sleep(0.2)  # Petite pause pour éviter les problèmes
    pyautogui.mouseDown()  # Clique et maintient enfoncé
    time.sleep(0.2)  # Attends un peu pour stabiliser le clic
    pyautogui.dragTo(1250, 1000, duration=1, button='left')  # Glisse jusqu'à la position finale
    pyautogui.mouseUp()  # Relâche le clic
    time.sleep(1)
    pyautogui.click(2219, 769)  # Ajuste ces coordonnées pour cliquer sur "Connecter"
    print("Comptes sélectionnés et connexion lancée.")