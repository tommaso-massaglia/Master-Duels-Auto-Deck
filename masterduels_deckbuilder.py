import time
import win32gui
import win32ui
import cv2
import numpy as np
from PIL import Image
from ctypes import windll
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import keyboard
import json
import requests
import pandas as pd
import argparse

m = PyMouse()
k = PyKeyboard()

hwnd = win32gui.FindWindow(None, 'masterduel')
rect = win32gui.GetWindowRect(hwnd)

# We then define a method to click inside the window using an event click
def clickwin(x, y):
    win32gui.SetForegroundWindow(hwnd) 
    time.sleep(0.05)
    m.click(rect[0]+x+10, rect[1]+y+10)
    m.click(rect[0]+x+10, rect[1]+y+10)

# This is used to keep track of what's on the window
def get_screenshot():
    left, top, right, bot = win32gui.GetClientRect(hwnd)
    w = right - left
    h = bot - top
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    return im

# Use openCV2 to find if the required button is on screen at the time and click it if it is
def isonscreen(small_image, large_image, conf = 0.85, click = True):
    res = cv2.matchTemplate(small_image, large_image, cv2.TM_CCOEFF_NORMED)
    min_v, max_v, min_pt, max_pt = cv2.minMaxLoc(res)
    if max_v > conf and click:
        clickwin(max_pt[0], max_pt[1])
        return True
    elif max_v > conf and not click:
        return True
    return False

def searchcard(cardname):
    time.sleep(0.05)
    k.press_keys([k.control_key, 'a'])
    time.sleep(0.05)
    k.press_key(k.delete_key)
    time.sleep(0.05)
    keyboard.write(cardname)
    time.sleep(0.05)
    k.press_key(k.enter_key) 
    
def addcard():
    while not isonscreen(foundcard, screenshot, conf=0.3, click=False):
        print('card not found')
    time.sleep(0.2)
    m.click(rect[0]+1470, rect[1]+433)
    while not isonscreen(addcardim, screenshot):
        print('addcard not found')

# Get the dictionary of cards
def card_db():
    response = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php")
    response.raise_for_status()
    return pd.DataFrame(json.loads(json.dumps(response.json()))['data'])[['id','name']]

# Get the card name fromm the ID
def get_card_name(id, card_db):
    return card_db[card_db['id'] == id].iloc[0][1]

# Read the YDK file
def read_ydk(fname):
    df = pd.read_csv(fname, header=None, names=['id'])
    ids = []
    for value in df['id']:
        if '!side' in value:
            continue
        elif value.isdigit():
            ids.append(int(value))
    return ids

# Import all the buttons screenshots
textsearch = cv2.imread('buttons/textsearch.png')
foundcard = cv2.imread('buttons/foundcard.png')
addcardim = cv2.imread('buttons/addcard.png')

database = card_db()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-ydk')
    args = parser.parse_args()
    
    for id in read_ydk(args.ydk):
        screenshot = get_screenshot()
        #screenshot.save('masterduels.jpg')
        screenshot = np.asarray(screenshot)[:, :, ::-1].copy() 
        
        if isonscreen(textsearch, screenshot):
            searchcard(get_card_name(id, database))
            time.sleep(0.05)
            addcard()
            time.sleep(0.05)
        