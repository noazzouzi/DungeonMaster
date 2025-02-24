import time
import pyautogui
import window
from pynput.keyboard import Controller, Key
import json

with open("config/config.json", "r", encoding="utf-8") as file:
    config = json.load(file)
displayCharacter = config["character_name"]
keyboard = Controller()

def invite():
    window.window(displayCharacter)
    time.sleep(2)

    # Étape 5 : Inviter la team dans le groupe (Alt + G), cliquer sur "Valider", puis appuyer sur F10 et F11
    keyboard.press(Key.alt)   # Appuyer sur Alt
    time.sleep(0.5)         # Petite pause avant de presser G
    keyboard.press('g')     # Appuyer sur G
    time.sleep(0.5)         # Petite pause pour éviter que G soit relâché trop tôt
    keyboard.release('g')   # Relâcher G
    time.sleep(0.2)         # Pause avant de relâcher Alt
    keyboard.release(Key.alt) # Relâcher Alt

    time.sleep(0.5)  # Petite pause
    pyautogui.click(1670, 880)  # Ajuste ces coordonnées si nécessaire pour "Valider"
    print("Invitation groupe... !")
    time.sleep(1)

    # Simuler F10 et F11
    keyboard.press(Key.f10)
    keyboard.release(Key.f10)

    time.sleep(0.5)  # Petite pause

    keyboard.press(Key.f11)
    keyboard.release(Key.f11)

    print("Touches envoyées : Alt+G, F10, F11")
    time.sleep(1)

    chibi_mode = (180, 50) # Passage en mode créature
    pyautogui.mouseDown(chibi_mode)
    time.sleep(0.2)
    pyautogui.mouseUp(chibi_mode)
    time.sleep(1)
    
    print("Tout est prêt, LETS GO !")
    time.sleep(3)