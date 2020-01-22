from pynput import keyboard
import time
from threading import *

class loop(Thread):
    def run(self):
        global controller
        while 42:
            if controller == True:
                print('hello')
                time.sleep(0.2)
            elif controller == False:
                time.sleep(0.05)

loop = loop()
controller = False
loop.start()

def on_press(key):
    global controller
    if key == keyboard.KeyCode(char='c'):
        controller = True
        print('Started')
    elif key == keyboard.KeyCode(char='v'):
        controller = False
        print('Stopped')
    # try:
    #     print('alphanumeric key {0} pressed'.format(
    #         key.char))
    # except AttributeError:
    #     print('special key {0} pressed'.format(
    #         key))

def on_release(key):
    global controller
    print('{0} released'.format(
        key))
    # if key == keyboard.Key.esc:
    #     # Stop listener
    #     return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
# listener = mouse.Listener(
#     on_press=on_press,
#     on_release=on_release)
# listener.start()
