import pyautogui
import time 

RECAP_POS = (2392, 250)

def close():
    pyautogui.mouseDown(RECAP_POS)
    time.sleep(0.2)
    pyautogui.mouseUp(RECAP_POS)