import npc
import time
import dungeon
import json
import keyboard
import detect_monster
import travel

def move(map):
    print("Moving to next map ! " + str(map))
    keyboard.press(map)
    keyboard.release(map)
    time.sleep(5)

def startDungeon(dungeonName):
    print(f"🎯 Donjon sélectionné : {dungeonName.capitalize()}")
    with open("config/dungeon/" + dungeonName + ".json", "r", encoding="utf-8") as file:
        config = json.load(file)

    NPC_POS = config["enter_dungeon"]["npc_pos"]  # Coordonnées du PNJ
    DIALOGUE_POS = config["enter_dungeon"]["dialogue_pos"]  # Coordonnées de la boîte de dialogue
    KEY_POS = config["enter_dungeon"]["key_pos"]  # Coordonnées de la boîte de dialogue

    # Délai entre les actions (à ajuster si nécessaire)
    DELAY = 1.5  
    LOADING_TIME = 3
    #step 1 : Talk to NPC and enter the dungeon
    npc.click(NPC_POS, DIALOGUE_POS, KEY_POS, DELAY)

    #step 2 : Wait for all characters to load the map
    time.sleep(LOADING_TIME)

    #step 3 : Start Dungeon Script
    MONSTER_1 = config["monsters"]["room1"]
    MONSTER_2  = config["monsters"]["room2"]
    MONSTER_3 = config["monsters"]["room3"]
    MONSTER_4 = config["monsters"]["room4"]
    BOSS      = config["monsters"]["boss"]
    dungeon.run(MONSTER_1, MONSTER_2, MONSTER_3, MONSTER_4, BOSS)

    #step 4 : Leave Dungeon
    NPC_POS = config["leave_dungeon"]["npc_pos"]  # Coordonnées du PNJ
    DIALOGUE_POS = config["leave_dungeon"]["dialogue_pos"]  # Coordonnées de la boîte de dialogue
    KEY_POS = config["leave_dungeon"]["key_pos"]  # Coordonnées de la boîte de dialogue
    npc.click(NPC_POS, DIALOGUE_POS, KEY_POS, DELAY)

def startZone(zoneName):
    print(f"🎯 Zone sélectionné : {zoneName.capitalize()}")
    with open("config/zone/" + zoneName + ".json", "r", encoding="utf-8") as file:
        config = json.load(file)
        
    monsters = config["monsterNames"]
    iteration = 0
    current_map = 0
    start_map = config["start_map"]
    print("Deplacement vers Map de départ: " + str(start_map))
    travel.travel(start_map)
    while True:
        detect_monster.click_box(monsters)
        time.sleep(0.5)
        iteration = iteration + 1
        print("iteration " + str(iteration))
        if iteration > 3:
                print("Map completed, to the next!")
                travel.travelTo(config["positions"][current_map])
                current_map = current_map + 1
                iteration = 0
                if current_map == len(config["maps"]):
                     print("Fin du trajet, remise à 0")
                     current_map = 0