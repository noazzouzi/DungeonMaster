import keyboard
import time
import json
import pyautogui
import cv2
import pytesseract

with open("config/config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

with open("config/zone/topaze.json", "r", encoding="utf-8") as file:
    zone = json.load(file)

# Définir le chemin de Tesseract OCR (si nécessaire)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

showMonster = config["showMonster"]
monsterNames = zone["monsterNames"]
pyautogui.mouseDown(showMonster)
# Prendre une capture d'écran de la région du jeu
screenshot = pyautogui.screenshot()
screenshot.save('show_monster.png')
screen = cv2.imread('show_monster.png')
time.sleep(0.5)
pyautogui.mouseUp(showMonster)

# Convertir en niveaux de gris
gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

# Appliquer un seuillage pour améliorer la reconnaissance
gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Utiliser Tesseract OCR pour extraire le texte
text = pytesseract.image_to_string(gray, lang="fra")  # "fra" pour français


for monsterName in monsterNames:
    print("here is text: " + text)
    if monsterName.lower() in text.lower():
        print("Trouvé.. ! " + monsterName)
        # Trouver la position du texte (bounding boxes)
        data = pytesseract.image_to_data(gray, lang="fra", output_type=pytesseract.Output.DICT)
        for i in range(len(data["text"])):
            if monsterName.lower() in data["text"][i].lower():
                x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
                print(data["text"][i], x, y, w, h)
                for j in range(50):
                    print("text " + str(j) + ": " + data["text"][i + j])
                # Déplacer la souris sous le texte (quelques pixels en bas)
                pyautogui.moveTo(x + w // 2, y * 2)  
                pyautogui.mouseDown(x + w // 2, y * 2)
                pyautogui.mouseUp(x + w // 2, y * 2)
                print("clicking in " + str(x + w // 2) + "," + str(y * 2))
                break

        time.sleep(0.5)