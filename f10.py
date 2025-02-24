import os
import time
import psutil
import pyautogui
import pygetwindow as gw
import window
import subprocess

time.sleep(3)
# Étape 5 : Inviter la team dans le groupe (Alt + G), cliquer sur "Valider", puis appuyer sur F10 et F11
pyautogui.hotkey("alt", "g")
time.sleep(1)
pyautogui.click(1670, 880)  # Ajuste ces coordonnées si nécessaire pour "Valider"
print("Invitation groupe... !")
time.sleep(1)

pyautogui.press("f10")
pyautogui.press("f11")
print("Touches F10 et F11 pressées.")
time.sleep(1)

chibi_mode = (180, 50) # Passage en mode créature
pyautogui.mouseDown(chibi_mode)
time.sleep(0.2)
pyautogui.mouseUp(chibi_mode)
time.sleep(1)

print("Tout est prêt, LETS GO !")