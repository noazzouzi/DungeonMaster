import keyboard
import time


time.sleep(3)

def move(map):
    keyboard.press(map)
    keyboard.release(map)

move('2')