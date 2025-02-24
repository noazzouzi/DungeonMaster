import pyautogui
import time

def click(npc_pos, dialogue_pos, key_pos, delay):
    pyautogui.mouseDown(npc_pos)
    time.sleep(0.2)
    pyautogui.mouseUp(npc_pos)
    time.sleep(delay)
    print("J'ai cliqué sur le PNJ")

    # Clique sur la boîte de dialogue
    pyautogui.click(dialogue_pos)
    time.sleep(delay)
    print("J'ai cliqué sur la demande de clé")

    if key_pos != None:
        # Clique sur la confirmation
        pyautogui.click(key_pos)
        time.sleep(delay)
        print("J'ai cliqué sur la confirmation")

    print("Attente chargement map...")