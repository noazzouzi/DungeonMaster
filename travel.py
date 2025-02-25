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

def move(pos):
    print("going " + str(pos))
    keyboard.press(pos)
    time.sleep(0.5)
    keyboard.release(pos)


def travelTo(pos):
    print("moving to : -> " + str(pos))
    match pos:
        case 'up': move('8')
        case 'down': move('5')
        case 'right': move('2')
        case 'left': move('1')