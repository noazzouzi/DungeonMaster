import cv2
import numpy as np
import pyautogui
import os
import time
import json
import pytesseract
import detect_fight

def find_and_click_monsters(folder_path):
    # Liste tous les fichiers dans le dossier contenant les images des monstres
    monster_images = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    
    # Prendre une capture d'écran de la région du jeu
    screenshot = pyautogui.screenshot()
    screenshot.save('game_screenshot.png')
    screen = cv2.imread('game_screenshot.png')

    # Traiter chaque image de monstre
    for monster_image in monster_images:
        template_path = os.path.join(folder_path, monster_image)
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        template_height, template_width = template.shape[:2]

        # Effectuer la correspondance de template
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Vérifier si la correspondance est assez bonne
        if max_val > 0.7:  # Seuil de correspondance, ajuster selon la précision souhaitée
            # Calculer la position centrale du template trouvé
            click_position = (max_loc[0] + template_width // 2, max_loc[1] + template_height // 2)

            # Cliquer sur le centre du monstre détecté
            pyautogui.mouseDown(click_position)
            time.sleep(0.2)
            pyautogui.mouseUp(click_position)
            print(f"Monstre trouvé et cliqué à {click_position} pour l'image {monster_image}.")
            break
        else:
            print(f"Monstre de l'image {monster_image} non trouvé.")

# Chemin vers le dossier contenant les images des monstres

""""
monsters_folder_path = 'images/kwakwa/boss'
find_and_click_monsters(monsters_folder_path)
"""

def click_box(monsterNames):
    with open("config/config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    # Définir le chemin de Tesseract OCR (si nécessaire)
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    showMonster = config["showMonster"]

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
        click_x = vertical  # Utiliser la position X du bouton
        click_y = box_bottom + 50  # Ajouter un petit décalage pour cliquer sous la boîte

        pyautogui.mouseDown(click_x, click_y)
        time.sleep(0.5)
        pyautogui.mouseUp(click_x, click_y)
        print(f"Clicking at {click_x}, {click_y} (bottom of monster box)")
        while detect_fight.is_combat_ready("images/spellbar.png") is True:
            print("En combat... Script en pause !")
            time.sleep(1)
    else:
        print("Boîte des monstres non détectée !")
