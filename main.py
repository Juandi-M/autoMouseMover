import time
import pyautogui

if __name__ == '__main__':
    width, height = pyautogui.size()
    while True:
        try:
            pyautogui.moveRel(0, 10)  # move mouse 10 pixels down
            time.sleep(0.01)
            pyautogui.moveRel(0, -10)  # drag mouse 10 pixels down
            time.sleep(59)
        except pyautogui.FailSafeException:
            pyautogui.FAILSAFE = False
            pyautogui.moveTo(width / 2, height / 2)
            pyautogui.FAILSAFE = True
            print("Shits fucked, moving to center")

