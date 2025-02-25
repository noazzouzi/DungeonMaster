import time
import json
import random
import cv2
import numpy as np
import pyautogui
import keyboard

# Charger la configuration
with open("config/zone/topaze.json", "r") as file:
    config = json.load(file)

monster_colors = config["monsterColors"]
map_directions = config["mapDirections"]
click_delay = (0.5, 1.0)
max_attempts = 5
total_attempts = 0
stop_script = False

def capture_screen():
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def find_monsters(image):
    detected_monsters = []
    for monster, colors in monster_colors.items():
        for hex_color in colors:
            hex_color = hex_color.lstrip("#")  # Supprime le #
            bgr_color = tuple(int(hex_color[i:i+2], 16) for i in (4, 2, 0))
            mask = cv2.inRange(image, np.array(bgr_color) - 10, np.array(bgr_color) + 10)
            coords = cv2.findNonZero(mask)
            if coords is not None:
                for pt in coords:
                    detected_monsters.append((pt[0][0], pt[0][1]))
    return detected_monsters

def click_on_monster():
    global total_attempts
    image = capture_screen()
    monsters = find_monsters(image)
    if monsters:
        x, y = random.choice(monsters)
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()
        time.sleep(0.1)
        pyautogui.mouseUp()
        time.sleep(random.uniform(*click_delay))
        total_attempts = 0
    else:
        total_attempts += 1

def detect_combat():
    image = capture_screen()
    # Ajouter ici une condition pour détecter le combat (ex: présence d'une interface spécifique)
    return False

def change_map():
    direction = random.choice(list(map_directions.keys()))
    key = map_directions[direction]
    keyboard.press_and_release(str(key))
    time.sleep(2)

def stop_script_callback():
    global stop_script
    stop_script = True
    print("Script arrêté par l'utilisateur.")

def main():
    global total_attempts, stop_script
    keyboard.add_hotkey("F2", stop_script_callback)
    while not stop_script:
        if detect_combat():
            print("Combat détecté, mise en pause du script.")
            time.sleep(10)
            continue
        
        click_on_monster()
        
        if total_attempts >= max_attempts:
            print("Aucun monstre trouvé, changement de map.")
            change_map()
            total_attempts = 0
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()
