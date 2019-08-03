import pyautogui
import pytesseract
import numpy as np
from PIL import Image
import re
import json
import tkinter as tk


class EncounterTracker:
    def __init__(self, master):
        self.bx = None
        self.lastMon = ''
        self.count = 0
        with open('files/encounters.json', 'r') as f:
            try:
                self.encounters = json.load(f)
            except json.decoder.JSONDecodeError:
                self.encounters = {}
            f.close()
        print(self.encounters)
        frame1 = tk.Frame()
        frame1.pack(side=tk.BOTTOM)
        frame2 = tk.Frame()
        frame2.pack(side=tk.LEFT)

        self.calibrate = tk.Button(frame1, text="Calibrate", command=self.reset)
        self.calibrate.pack(side=tk.LEFT)
        self.exit = tk.Button(frame1, text="Exit", command=root.quit)
        self.exit.pack(side=tk.RIGHT)

        self.startTracking = tk.Button(frame2, text="Start Tracking", fg="WHITE", bg="GREEN", command=self.main)
        self.startTracking.pack(side=tk.TOP)

        self.label1 = tk.Label(frame2, text="Last Encounter:")
        self.label1.pack()

        self.lastEncounter = tk.Label(frame2, text="No encounters yet!")
        self.lastEncounter.pack(side=tk.BOTTOM)

        self.encounterBox = tk.Listbox(root)
        self.encounterBox.pack(side=tk.TOP)
        for k, v in self.encounters.items():
            self.encounterBox.insert(tk.END, f"{k}: {v}")

    def reset(self):
        bx = pyautogui.locateOnScreen('files/vs.png')
        self.bx = bx

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
            root.after(2000, a.main)
            return
        if self.lastMon == '':
            p = re.split(' ', t)[-1]
            if p != '':
                if p.lower() not in dex.keys():
                    root.after(2000, a.main)
                    return
                print(p)
                self.lastEncounter.configure(text=p)
                try:
                    self.encounters[p] += 1
                except KeyError:
                    self.encounters[p] = 1
                with open('files/encounters.json', 'w+') as f:
                    json.dump(self.encounters, f)
                    f.close()
                self.encounterBox.delete(0, tk.END)
                for k, v in self.encounters.items():
                    self.encounterBox.insert(tk.END, f"{k}: {v}")
            self.count += 1
        self.lastMon = t
        root.after(2000, a.main)


pytesseract.pytesseract.tesseract_cmd = r'ocr\tesseract.exe'
with open('files/pokedex.json', 'r') as dexfile:
    dex = json.load(dexfile)
    dexfile.close()
root = tk.Tk()
root.title("PRO Farm Assistant")
a = EncounterTracker(root)
root.mainloop()
