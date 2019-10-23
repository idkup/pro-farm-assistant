import pyautogui
import pytesseract
import numpy as np
from PIL import Image
import re
import json
import tkinter as tk
from tkinter import messagebox


class EncounterTracker:
    def __init__(self, master):
        self.bx = None
        self.lastMon = ''
        self.count = 0
        self.tracking = False
        with open('files/encounters.json', 'r') as f:
            try:
                self.encounters = json.load(f)
            except json.decoder.JSONDecodeError:
                self.encounters = {}
            f.close()
        frame1 = tk.Frame(master)
        frame1.pack(side=tk.BOTTOM)
        frame2 = tk.Frame(master)
        frame2.pack(side=tk.BOTTOM)
        frame3 = tk.Frame(master)
        frame3.pack(side=tk.LEFT)

        self.calibrate = tk.Button(frame1, text="Calibrate", command=self.recalibrate)
        self.calibrate.pack(side=tk.LEFT)
        self.exit = tk.Button(frame1, text="Exit", command=root.quit)
        self.exit.pack(side=tk.RIGHT)

        self.message = tk.Label(frame2, text=None)
        self.message.pack()

        self.startTracking = tk.Button(frame3, text="Start Tracking", fg="WHITE", bg="GREEN", command=self.start)
        self.startTracking.pack(side=tk.TOP)

        self.stopTracking = tk.Button(frame3, text="Stop Tracking", fg="WHITE", bg="RED", command=self.stop)
        self.stopTracking.pack()

        self.label1 = tk.Label(frame3, text="Last Encounter:")
        self.label1.pack()

        self.lastEncounter = tk.Label(frame3, text="No encounters yet!")
        self.lastEncounter.pack(side=tk.BOTTOM)

        self.encounterBox = tk.Listbox(root)
        self.encounterBox.pack(side=tk.TOP)

        for k, v in self.encounters.items():
            self.encounterBox.insert(tk.END, f"{k}: {v}")

    def recalibrate(self):
        self.bx = pyautogui.locateOnScreen('files/vs.png')
        if self.bx:
            self.message.configure(text="Calibrated!", fg="BLACK")
        else:
            self.message.configure(text="Calibration failed!", fg="RED")

    def stop(self):
        if self.tracking is False:
            return
        self.tracking = False
        self.message.configure(text="Tracking ended.", fg="RED")

    def start(self):
        if self.tracking is True:
            return
        self.tracking = True
        self.message.configure(text="Tracking started.", fg="GREEN")
        root.after(500, self.main)

    def main(self):
        self.message.configure(text="")
        if not self.bx:
            self.recalibrate()
        sc = pyautogui.screenshot().crop((self.bx.left, self.bx.top, self.bx.left + 500, self.bx.top + self.bx.height))
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
            root.after(1000, a.main)
            return
        if self.lastMon == '':
            p = re.split(' ', t)[-1]
            if p != '':
                if p.lower() not in dex.keys():
                    print(p)
                    root.after(1000, self.main)
                    return
                if p == 'Froakie':
                    tk.messagebox.showwarning('Target Pokemon Alert', f'{p} has spawned!')
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
        if self.tracking is True:
            root.after(1000, self.main)


pytesseract.pytesseract.tesseract_cmd = r'ocr\tesseract.exe'
with open('files/pokedex.json', 'r') as dexfile:
    dex = json.load(dexfile)
    dexfile.close()
root = tk.Tk()
root.title("PRO Farm Assistant")
a = EncounterTracker(root)
root.mainloop()
