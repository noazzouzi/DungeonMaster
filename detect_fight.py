import cv2
import numpy as np
import pyautogui
import time

def is_combat_ready(spellbar_image_path):
    # Prendre une capture d'écran et charger l'image de la barre de sorts
    screenshot = pyautogui.screenshot()
    screenshot.save('fight_screenshot.png')
    screen = cv2.imread('fight_screenshot.png', cv2.IMREAD_COLOR)
    spellbar_template = cv2.imread(spellbar_image_path, cv2.IMREAD_COLOR)

    # Effectuer la correspondance de template
    result = cv2.matchTemplate(screen, spellbar_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    print("Recherche barre de sorts...")
    # Retourner vrai si la barre de sorts est détectée
    spellbar = max_val > 0.4
    print("Spellbar found : " + str(spellbar))
    return spellbar