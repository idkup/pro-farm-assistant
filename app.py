import pyautogui
import pytesseract
import time
import numpy as np
from PIL import Image
import re
import json


class EncounterTracker:
    def __init__(self):
        bx = pyautogui.locateOnScreen('files/vs.png')
        self.bx = bx
        self.lastMon = ''
        self.count = 0
        with open('files/encounters.json', 'w+') as f:
            try:
                self.encounters = json.load(f)
            except json.decoder.JSONDecodeError:
                self.encounters = {}
            f.close()
        print(self.encounters)

    def main(self):
        sc = pyautogui.screenshot().crop((self.bx.left, self.bx.top, self.bx.left + 250, self.bx.top + self.bx.height))
        sc = sc.convert('RGBA')
        data = np.array(sc)
        r, g, b, t = data.T
        out_areas = r <= 200
        text_areas = r > 200
        data[..., :-1][out_areas.T] = (252, 252, 252)
        data[..., :-1][text_areas.T] = (0, 0, 0)
        sc = Image.fromarray(data)
        t = pytesseract.image_to_string(sc)
        if 'Wild' not in t and t != '':
            return
        if self.lastMon == '':
            p = re.split(' ', t)[-1]
            if p != '':
                if p.lower() not in dex.keys():
                    time.sleep(2)
                    return
                print(p)
                try:
                    self.encounters[p] += 1
                except KeyError:
                    self.encounters[p] = 1
                with open('files/encounters.json', 'w+') as f:
                    json.dump(self.encounters, f)
                    f.close()
            self.count += 1
        self.lastMon = t
        time.sleep(2)


pytesseract.pytesseract.tesseract_cmd = r'ocr\tesseract.exe'
with open('files/pokedex.json', 'r') as dexfile:
    dex = json.load(dexfile)
    dexfile.close()
a = EncounterTracker()
while True:
    for i in range(10):
        a.main()
    print(a.encounters)
