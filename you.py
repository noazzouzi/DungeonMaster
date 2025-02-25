import time
import random
import pyautogui
import cv2
import numpy as np
import pytesseract
import json
import detect_fight
import travel
import keyboard

# Configuration de Tesseract (chemin à adapter selon l'installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
ite = 0

def capture_screen():
    with open("config/config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    showMonster = config["showMonster"]
    # Afficher la boîte des monstres
    pyautogui.mouseDown(showMonster)
    time.sleep(0.5)  # Attendre l'affichage de la boîte
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    pyautogui.mouseUp(showMonster)
    return frame

def detect_monster_boxes(frame, zone):
    with open("config/zone/" + zone + ".json", "r", encoding="utf-8") as file:
        zone = json.load(file)
    monster_names = set(zone["monsterNames"])
    special_monsters = set(zone["specialMonsters"])
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text_boxes = []
    
    # OCR pour détecter les boîtes contenant du texte
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
    
    for i in range(len(data['text'])):
        text = data['text'][i].strip()
        if text and any(monster in text for monster in monster_names):  # Détection spécifique
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            text_boxes.append((x, y, w, h))
    
    return text_boxes

def find_monster_to_click(text_boxes, ite):
    print("text boxes : " + str(text_boxes))
    if not text_boxes:
        return None
    

    # Sélectionner une boîte de texte au hasard
    if len(text_boxes) == 0 or ite >= len(text_boxes):
        box = random.choice(text_boxes)
    else:
        box = text_boxes[ite]
    print("box " + str(ite) + ": " + str(box))
    x, y, w, h = box
    
    # Estimer la position du monstre sous la boîte (ajuster selon la hauteur des boîtes de texte)
    monster_x = (x + w // 2) + 30
    monster_y = y + h + 100  # Ajustement vertical
    
    return (monster_x, monster_y)

def main_loop():
    with open("config/zone/topaze.json", "r", encoding="utf-8") as file:
        zone = json.load(file)
    iteration = 0
    current_map = 0
    positions = zone["positions"]

    time.sleep(1)
    ite = 0
    while True:
        
        frame = capture_screen()
        text_boxes = detect_monster_boxes(frame, "topaze")
        monster_pos = find_monster_to_click(text_boxes, ite)
        ite = ite + 1
        if ite == len(text_boxes) - 1:
            ite = 0
        if monster_pos:
            x, y = monster_pos
            pyautogui.mouseDown(x, y)
            time.sleep(0.5)
            pyautogui.mouseUp(x, y)
            print(f'Clique sur monstre à ({x}, {y})')
            while detect_fight.is_combat_ready("images/spellbar.png") is True:
                print("En combat... Script en pause !")
                time.sleep(3)
        iteration = iteration + 1
        if iteration > 3:
            print("Move to next map")
            time.sleep(1.5)
            pyautogui.mouseDown(100, 550)
            time.sleep(0.5)
            pyautogui.mouseUp(100, 550)
            time.sleep(0.5)
            travel.travelTo(positions[current_map])
            time.sleep(2)
            current_map = current_map + 1
            iteration = 0
        if current_map == len(positions):
            current_map = 0
        time.sleep(0.5)  # Évite de spammer trop vite

if __name__ == "__main__":
    main_loop()
