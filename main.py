import start
import window
import time
import restart_game
import keyboard
import time
import json

category = input("Donjon ou Zone ?").strip().lower()
script = input("Entrez le nom du script (Donjon/Zone) : ").strip().lower()

paused = False  # Variable pour suivre l'état de pause

def toggle_pause():
    global paused
    paused = not paused  # Inverser l'état de pause
    if paused:
        print("⏸ Script en pause. Appuyez sur 'p' pour reprendre.")
    else:
        print("▶ Script repris.")

# Associer la touche "F8" à la fonction toggle_pause
keyboard.add_hotkey("F8", toggle_pause)

print("Appuyez sur 'F8' pour mettre en pause / reprendre le script.")

with open("config/config.json", "r", encoding="utf-8") as file:
    config = json.load(file)
display = config["character_name"]
runs = 1
max_runs = 30

#step 0 : Bring Dofus page upfront
window.window(display)
while runs < max_runs:
    if not paused:
        print("Run #" + str(runs) + " of " + str(max_runs))
        match category:
            case "dungeon": start.startDungeon(script)
            case "zone": start.startZone(script)
        time.sleep(3)
        runs = runs + 1
        if runs % 5 == 0:
            restart_game.restart()
    else:
        time.sleep(0.1)  # Éviter une boucle infinie trop gourmande en CPU