import time
import json
import pyautogui
import cv2
import pytesseract

# Charger les configurations
with open("config/config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

with open("config/zone/topaze.json", "r", encoding="utf-8") as file:
    zone = json.load(file)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

showMonster = config["showMonster"]
monsterNames = zone["monsterNames"]

# Afficher la boîte des monstres
pyautogui.mouseDown(showMonster)
time.sleep(0.5)  # Attendre l'affichage de la boîte
screenshot = pyautogui.screenshot()
screenshot.save('show_monster.png')
screen = cv2.imread('show_monster.png')
pyautogui.mouseUp(showMonster)

# Convertir en niveaux de gris et améliorer la reconnaissance
gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Extraire le texte et leurs positions
data = pytesseract.image_to_data(gray, lang="fra", output_type=pytesseract.Output.DICT)

box_top, box_bottom = None, None
vertical = None

# Détection de la boîte complète
for i in range(len(data["text"])):
    text = data["text"][i].strip().lower()
    x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]

    # Détecter le haut de la boîte avec "Niveau"
    if "niveau" in text:
        print("Niveau : " + str(x) + ", " + str(y) + ", " + str(w), ", " + str(h))
        
        if box_top is None or y < box_top:
            box_top = y

    # Détecter le bas de la boîte avec les noms des monstres
    for monsterName in monsterNames:
        if monsterName.lower() in text:
            print("monster : " + str(monsterName) + " / " + str(x) + ", " + str(y) + ", " + str(w), ", " + str(h))
            
            if box_bottom is None or (y + h) > box_bottom:
                vertical = x + w
                box_bottom = y + h  # Bas du dernier monstre détecté

# Si la boîte est bien détectée, cliquer en bas
if box_top is not None and box_bottom is not None:
    print("click : " + str(vertical) + ", " + str(box_bottom + 500))
    click_x = vertical + 10  # Utiliser la position X du bouton
    click_y = box_bottom + 50  # Ajouter un petit décalage pour cliquer sous la boîte

    pyautogui.mouseDown(click_x, click_y)
    time.sleep(0.5)
    pyautogui.mouseUp(click_x, click_y)
    print(f"Clicking at {click_x}, {click_y} (bottom of monster box)")
else:
    print("Boîte des monstres non détectée !")
