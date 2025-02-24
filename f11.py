from pynput.keyboard import Controller, Key
import time
import pyautogui

keyboard = Controller()

# Attendre pour éviter tout problème de timing
time.sleep(3)

# Simuler Alt + G
with keyboard.pressed(Key.alt):
    keyboard.press('g')
    keyboard.release('g')

time.sleep(0.5)  # Petite pause
pyautogui.click(1670, 880)  # Ajuste ces coordonnées si nécessaire pour "Valider"
print("Invitation groupe... !")
time.sleep(1)

# Simuler F10 et F11
keyboard.press(Key.f10)
keyboard.release(Key.f10)

time.sleep(0.5)  # Petite pause

keyboard.press(Key.f11)
keyboard.release(Key.f11)

print("Touches envoyées : Alt+G, F10, F11")
time.sleep(1)

chibi_mode = (180, 50) # Passage en mode créature
pyautogui.mouseDown(chibi_mode)
time.sleep(0.2)
pyautogui.mouseUp(chibi_mode)
time.sleep(1)
