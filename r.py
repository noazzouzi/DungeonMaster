import keyboard 
import pyautogui
import time

def move(pos):
    keyboard.press(pos)
    time.sleep(0.5)
    keyboard.release(pos)

time.sleep(1)
move('2')
time.sleep(1)
move('1')
time.sleep(1)
move('5')
time.sleep(1)
move('8')