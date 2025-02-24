import cv2
import numpy as np
import pyautogui
import os
import time

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