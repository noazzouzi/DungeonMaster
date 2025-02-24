import json
import pyautogui
import time
import keyboard

def travel(map):
    with open("config/config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    chat = config["chat"]

    time.sleep(3)
    pyautogui.mouseDown(chat)
    time.sleep(0.2)
    pyautogui.mouseUp(chat)
    time.sleep(0.5)
    keyboard.write("/travel " + map)
    time.sleep(0.5)
    keyboard.press_and_release('enter')  # Premier appui
    time.sleep(0.5)  # Attendre 0.5 seconde
    keyboard.press_and_release('enter')  # Deuxième appui
    time.sleep(10)