import fight_recap
import time
import detect_monster
import detect_fight
import pyautogui

def salle(monster_path, isBoss=False):
    start_time = time.time()  # Enregistre le moment où la recherche commence
    elapsed_time = 0
    print("Démarrage calcul temps écoulé..." + str(elapsed_time))
    while detect_fight.is_combat_ready("images/spellbar.png") is False and elapsed_time < 30:
        current_time = time.time()
        elapsed_time = current_time - start_time
        print("Recherche monstre... " + monster_path.split("/")[1] + " " + monster_path.split("/")[2])
        detect_monster.find_and_click_monsters(monster_path)
        print("En attente de combat...")
        print ("Temps écoulé... " + str(elapsed_time) + "s")
        time.sleep(1)  # Pause entre les recherches pour limiter la charge sur le CPU

    if elapsed_time < 40:
        if isBoss is True:
            time.sleep(40)
        time.sleep(30)
    else:
        time.sleep(1)     

    fight_recap.close()
    print("Combat fini... " + monster_path.split("/")[1] + " " + monster_path.split("/")[2] + " / " + str(elapsed_time) + "s")
    # Déplace la souris de 100 pixels à droite et 50 pixels vers le bas par rapport à sa position actuelle
    pyautogui.moveRel(500, 50, duration=1)

