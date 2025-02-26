import time
import json
import random
import cv2
import numpy as np
import pyautogui
import keyboard
import pytesseract
import window
import difflib

# Charger la configuration
with open("config/zone/topaze.json", "r", encoding="utf-8") as file:
    config = json.load(file)

monster_colors = config["monsterColors"]
click_delay = (0.5, 1.0)
max_attempts = 5
total_attempts = 0
stop_script = False

# Liste des directions à suivre pour changer de map
directions_list = list(config["positions"])
direction_index = 0  # Pour suivre l'indice dans la liste

def capture_screen():
    # Résolution de l'écran
    screen_width, screen_height = pyautogui.size()

    # Dimensions de la zone à capturer (800x1200)
    capture_width = 1200
    capture_height = 1000  # Garder la même hauteur, mais prendre plus du haut

    # Calcul des coordonnées du coin supérieur gauche pour la zone
    start_x = (screen_width - capture_width) // 2
    start_y = (screen_height - capture_height) // 2 - 100  # Décalage vers le haut pour capturer plus du haut

    # Capture d'écran dans la zone de 1200x800
    screenshot = pyautogui.screenshot(region=(start_x, start_y, capture_width, capture_height))
    
    # Sauvegarder le screenshot pour vérifier
    screenshot.save("screenshot_800x1200_more_top.png")
    
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR), start_x, start_y

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

def read_monster_text():
    # Capturer une petite zone autour du monstre pour lire le texte
    # Les coordonnées peuvent être ajustées en fonction de la position du texte affiché
    screen_width, screen_height = pyautogui.size()
    capture_width = 1200  # Ajuster cette largeur en fonction de la taille du texte
    capture_height = 1000  # Hauteur pour capturer le texte affiché

    # Calcul des coordonnées du coin supérieur gauche pour la zone
    start_x = (screen_width - capture_width) // 2
    start_y = (screen_height - capture_height) // 2 - 100  # Décalage vers le haut pour capturer plus du haut

    # Capture de la zone autour du monstre
    screenshot = pyautogui.screenshot(region=(start_x, start_y, capture_width, capture_height))
    screenshot_np = np.array(screenshot)
    screenshot.save("screenshot_text.png")

    # Utilisation de pytesseract pour extraire le texte de l'image
    text = pytesseract.image_to_string(screenshot_np)

    # Sauvegarder la capture pour vérifier si l'OCR fonctionne bien
    cv2.imwrite("screenshot_text.png", screenshot_np)

    return text.strip()  # Nettoyer le texte (retirer espaces, retours à la ligne)

def click_on_monster():
    global total_attempts
    image, start_x, start_y = capture_screen()
    monsters = find_monsters(image)

    # Liste des monstres acceptés dans la config
    accepted_monster_names = config["acceptedMonsters"]

    if monsters:
        # Choisir un monstre et ajuster les coordonnées par rapport à la zone capturée
        x, y = random.choice(monsters)
        # Ajuster les coordonnées en fonction du coin supérieur gauche de la capture
        x += start_x
        y += start_y

        # Déplacer la souris sur le monstre sans cliquer pour afficher le texte
        pyautogui.moveTo(x, y)
        time.sleep(0.1)

        # Lire le texte affiché (à adapter selon l'outil ou la méthode de capture de texte)
        monster_text = read_monster_text()

        # Vérifier si le nom du monstre est dans la liste des monstres acceptés
        if any(accepted_monster.lower() in monster_text.lower() for accepted_monster in accepted_monster_names):
            # Si le nom du monstre est valide, on clique
            pyautogui.mouseDown()
            time.sleep(0.1)
            pyautogui.mouseUp()
            #time.sleep(random.uniform(*click_delay))
            print(f"Monstre {monster_text} cliqué !")
            time.sleep(3)  # Attendre 3 secondes (ajuste la durée si nécessaire)
        else:
            # Si le nom du monstre n'est pas valide, déplacer la souris à gauche pour éviter de cliquer
            pyautogui.moveTo(x - 50, y)  # Déplacer à gauche
            print(f"Monstre {monster_text} ignoré.")

    print(f"Iteration #{total_attempts} of {max_attempts}")
    total_attempts += 1


def capture_screen_for_combat():
    # Résolution de l'écran
    screen_width, screen_height = pyautogui.size()

    # Capturer une zone réduite du bas de l'écran (600x200)
    capture_width = 1200
    capture_height = 800  # Plus petite hauteur concentrée vers le bas de l'écran

    # Calculer les coordonnées du coin supérieur gauche pour la zone (proche du bas de l'écran)
    start_x = (screen_width - capture_width) // 2
    start_y = screen_height - capture_height  # Commencer à partir du bas de l'écran

    # Capture d'écran dans la zone réduite
    screenshot = pyautogui.screenshot(region=(start_x, start_y, capture_width, capture_height))
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


def detect_combat():
    # Capture d'écran de l'interface actuelle
    image = capture_screen_for_combat()

    # Charger l'image de référence de la barre des sorts
    sort_bar = cv2.imread("images/spellbar.png", cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), sort_bar, cv2.TM_CCOEFF_NORMED)
    
    # Définir un seuil de correspondance (ici, 0.8 peut être ajusté selon le test)
    threshold = 0.5
    locations = np.where(result >= threshold)

    # Si des correspondances sont trouvées, cela signifie qu'un combat est lancé
    return len(locations[0]) > 0

def correct_map_name(detected_name, allowed_maps):
    """Corrige le nom de la map détectée en trouvant la plus proche dans la liste des maps valides."""
    closest_match = difflib.get_close_matches(detected_name, allowed_maps, n=1, cutoff=0.6)
    return closest_match[0] if closest_match else detected_name

def get_current_map(allowed_maps):
    """Utilise OCR pour lire le nom de la map en haut à gauche de l'écran avec amélioration de l'image."""
    screen_width, screen_height = pyautogui.size()

    # Capturer une petite zone en haut à gauche pour obtenir le nom de la map
    capture_width = 500  
    capture_height = 50  
    start_x = 10  
    start_y = 70  

    # Capture d'écran
    screenshot = pyautogui.screenshot(region=(start_x, start_y, capture_width, capture_height))
    screenshot_np = np.array(screenshot)
    screenshot.save("current_map.png")

    # Conversion en niveaux de gris
    gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

    # Appliquer un seuillage adaptatif pour améliorer le contraste
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Sauvegarder l'image pour debug (optionnel)
    cv2.imwrite("screenshot_map_processed.png", processed)

    # OCR
    map_text = pytesseract.image_to_string(processed, config="--psm 7").strip()
    map_text = correct_map_name(map_text, allowed_maps)

    return map_text



def check_map_validity():
    """Vérifie si la map actuelle est autorisée, sinon retourne à la position de départ."""
    allowed_maps = config["allowedMaps"]
    current_map = get_current_map(allowed_maps)
    print("maps autorisés : " + str(allowed_maps))
    print("current map : "  + str(current_map))
    if current_map not in allowed_maps:
        print(f"Map inconnue ({current_map}), retour à la map de départ.")
        return_to_start()

def travel(map):
    with open("config/config.json", "r", encoding="utf-8") as file:
        conf = json.load(file)

    chat = conf["chat"]

    time.sleep(1)
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

def return_to_start():
    """Effectue une série de déplacements pour revenir à la map initiale."""
    start_path = config["start_map"]  # Une liste d'actions pour retourner (ex: ["left", "up", "right"])
    travel(start_path)
    print("Retour à la map de départ terminé.")

def map_direction(direction):
    print("Moving " + str(direction).lower() + " !")
    match str(direction).lower():
        case 'up': return '8'
        case 'down': return '5'
        case 'right': return '2'
        case 'left': return '1'

def change_map():
    global direction_index
    # Obtenir la direction à partir de la liste
    direction = directions_list[direction_index]
    key = map_direction(direction)
    keyboard.press_and_release(str(key))
    time.sleep(2)

    # Mettre à jour l'index pour la prochaine direction
    direction_index = (direction_index + 1) % len(directions_list)  # Revenir à 0 si on atteint la fin de la liste

def stop_script_callback():
    global stop_script
    stop_script = True
    print("Script arrêté par l'utilisateur.")

def main():
    global total_attempts, stop_script
    keyboard.add_hotkey("F2", stop_script_callback)
    
    with open("config/config.json", "r") as file:
        conf = json.load(file)
    window.window(conf["character_name"])
    while not stop_script:
        check_map_validity()
        # Vérifier si un combat est lancé
        if detect_combat():
            print("Combat détecté ! Le script est en pause...")
            while detect_combat():
                time.sleep(1)  # Attendre que le combat soit terminé
            print("Combat terminé, le script reprend.")

        click_on_monster()
        
        if total_attempts >= max_attempts:
            print("Aucun monstre trouvé, changement de map.")
            change_map()
            total_attempts = 0
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()
