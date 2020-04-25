import ctypes
from ctypes import wintypes
import time
from threading import *
import threading 
from pynput import keyboard
from pynput.mouse import Controller
import random 
import sys 
import pyautogui 

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0

# List of all codes for keys:
# # msdn.microsoft.com/en-us/library/dd375731
UP = 0x26
DOWN = 0x28
LEFT = 0x25
W = 0x57
A = 0x41
S = 0x53
D = 0x44
Z = 0x5A
ESC = 0x1B
SPACE = 0x20

class keyLoop(Thread):
    def run(self):
        global controller
        global loops
        loops = 0
        while 42:
            if controller == True: ## controller toggle is bound in the on_press() listener
                pyautogui.click(button='right')
                pyautogui.click(button='middle')
                loops += 1
            elif controller == False:
                time.sleep(0.05)
    
class scroller(Thread):
    def run(self):
        global scroller
        global loops
        loops = 0
        while 42:
            if scroller == True:
                pyautogui.scroll(-5000)
                loops += 1
            elif controller == False:
                time.sleep(0.05)

def on_press(key):
    global controller
    global holder 
    global scroller 
    global loops, sTime, eTime 
    if key == keyboard.KeyCode(char='c'): ## keyboard listener to toggle global controller
        if controller == True:
            eTime = time.time() ## log time for statistics printout
            controller = False ## switch controller 
            print(f'Stopped at {time.ctime()} with {round(eTime - sTime, 2)} seconds runtime and a total of {loops} loops.')
            # loops = 0
        elif controller == False:
            sTime = time.time() ## log time for statistics printout
            controller = True ## switch controller
            print(f'Started at {time.ctime(sTime)}.')

    if key == keyboard.KeyCode(char='v'): ## keyboard listener to toggle global controller
        if holder == True:
            eTime = time.time() ## log time for statistics printout
            pyautogui.mouseUp(button='right')
            holder = False ## switch controller 
            print(f'Stopped at {time.ctime()} with {round(eTime - sTime, 2)} seconds runtime and a total of {loops} loops.')
            # loops = 0
        elif holder == False:
            sTime = time.time() ## log time for statistics printout
            pyautogui.mouseDown(button='right')
            print(f'Started at {time.ctime(sTime)}.')

    if key == keyboard.KeyCode(char='b'): ## keyboard listener to toggle global controller
        if scroller == True:
            eTime = time.time() ## log time for statistics printout
            scroller = False ## switch controller 
            print(f'Stopped at {time.ctime()} with {round(eTime - sTime, 2)} seconds runtime and a total of {loops} loops.')
            # loops = 0
        elif scroller == False:
            sTime = time.time() ## log time for statistics printout
            scroller = True 
            print(f'Started at {time.ctime(sTime)}.')


# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

if __name__ == "__main__":
    sTime = time.time()
    eTime = time.time() 
    kLoop = keyLoop() ## create keyLoop object 
    scrlr = scroller() 
    controller = False ## set controller to not fuck shit up 
    scroller = False 
    holder = False 
    killer = False ## experimental feature, currently removed 
    kLoop.start() ## start keyLoop (key spammer) as own thread, controlled by controller 
    scrlr.start() 
    with keyboard.Listener( 
            on_press=on_press) as listener: ## start listener for toggling controller via keypress 
        listener.join()
