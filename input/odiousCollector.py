import time
import autoit
import pyautogui as pygui

def click():
    screenX, screenY = pygui.size()
    x = screenX/2
    y = screenY/2
    autoit.mouse_click('left', int(x), int(y), 1)

if __name__ == '__main__':
    click()
