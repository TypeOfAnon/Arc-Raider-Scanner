import cv2
import numpy as np
from PIL import ImageGrab
import ctypes
import tkinter as tk
from pathlib import Path
import os
import sys

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    ctypes.windll.user32.SetProcessDPIAware()

QUEST_ITEMS = {'antiseptic', 'arc_alloy', 'battery', 'durable_cloth', 'fertilizer', 'great_mullein', 'hornet_driver', 'leaper_pulse_unit', 'flow_controller', 'power_rod', 'rocketeer_driver', 'wires', 'snitch_scanner', 'surveyor_vault', 'syringe', 'wasp_driver', 'water_pump', 'magnetron'}
PROJECT_ITEMS = {'rubber_parts', 'metal_parts', 'arc_alloy', 'durable_cloth', 'battery', 'electrical_components', 'wires', 'sensors', 'steel_spring', 'advanced_electrical_components', 'humidifier', 'light_bulb', 'cooling_fan', 'leaper_pulse_unit', 'magnetic_accelerator', 'exodus_modules'}
WORKSHOP_ITEMS = {'dog_collar', 'lemon', 'apricot', 'prickly_pear', 'olives', 'cat_bed', 'mushroom', 'very_comfortable_pillow', 'metal_parts', 'rubber_parts', 'rusted_tools', 'mechanical_components', 'wasp_driver', 'rusted_gear', 'advanced_mechanical_components', 'sentinel_firing_core', 'plastic_parts', 'fabric', 'power_cable', 'electrical_components', 'industrial_battery', 'advanced_electrical_components', 'bastion_cell', 'chemicals', 'synthesized_fuel', 'crude_explosives', 'pop_trigger', 'laboratory_reagents', 'explosive_compound', 'cracked_bioscanner', 'tick_pod', 'rusted_shut_medical_kit', 'damaged_heat_sink', 'fried_motherboard', 'arc_powercell', 'toaster', 'arc_motion_core', 'fireball_burner', 'motor', 'arc_circuitry', 'bombardier_cell'}

def get_category_style(name):
    n = name.lower().strip().replace(" ", "_")
    found_cats = []
    if n in QUEST_ITEMS: found_cats.append("QUEST")
    if n in PROJECT_ITEMS: found_cats.append("PROJ")
    if n in WORKSHOP_ITEMS: found_cats.append("WORK")
    if not found_cats: found_cats.append("ITEM")
    
    if "QUEST" in found_cats: color = (50, 50, 255)
    elif "PROJ" in found_cats: color = (0, 165, 255)
    elif "WORK" in found_cats: color = (50, 255, 50)
    else: color = (200, 200, 200)
    
    return color, " - ".join(found_cats)

class ArcRaiderScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Arc Raider Scanner - Made by Santazer")
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', 'pink')
        
        self.win_w, self.win_h = 550, 920
        self.win_x, self.win_y = 300, 40
        self.root.geometry(f"{self.win_w}x{self.win_h}+{self.win_x}+{self.win_y}")
        self.root.configure(bg="#000000")
        
        self.sift = cv2.SIFT_create()
        self.icons_db = []
        self.load_icons()

        self.header = tk.Frame(self.root, bg="#000000", pady=20)
        self.header.pack(side="top", fill="x")

        self.btn_scan = tk.Button(self.header, text="TARA", command=self.scan, 
                                 bg="#000000", fg="#00ff9d", font=("Segoe UI Black", 14),
                                 relief="flat", bd=2, highlightthickness=2, 
                                 highlightbackground="#00ff9d", cursor="hand2", width=15)
        self.btn_scan.pack()
        
        self.outline = tk.Frame(self.root, bg="#00f2ff", padx=2, pady=2)
        self.outline.pack(fill="both", expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(self.outline, bg='pink', highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.footer = tk.Frame(self.root, bg="#000000", pady=10)
        self.footer.pack(side="bottom", fill="x")

        self.signature = tk.Label(self.footer, text="SANTAZER TARAFINDAN YAPILDI", 
                                 fg="#ffffff", bg="#000000", font=("Segoe UI Black", 10))
        self.signature.pack()

        self.version = tk.Label(self.footer, text="v0.1 BETA", 
                               fg="#555555", bg="#000000", font=("Arial", 8, "bold"))
        self.version.pack(side="right", padx=10)

        self.root.bind("<Configure>", self.update_position)

    def update_position(self, event=None):
        self.win_x = self.root.winfo_x()
        self.win_y = self.root.winfo_y()
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("grid")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w < 10: return
        for i in range(1, 4):
            x = i * (w / 4)
            self.canvas.create_line(x, 0, x, h, fill="#00f2ff", tags="grid", width=2)
        for i in range(1, 6):
            y = i * (h / 6)
            self.canvas.create_line(0, y, w, y, fill="#00f2ff", tags="grid", width=2)

    def load_icons(self):
        p = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        ip = Path(p) / "icons"
        if not ip.exists(): return
        for f in ip.glob("*.png"):
            img = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE)
            kp, des = self.sift.detectAndCompute(img, None)
            if des is not None: self.icons_db.append({"name": f.stem, "kp": kp, "des": des})

    def scan(self):
        self.btn_scan.config(text="TARANIYOR...", state="disabled", fg="#ffcc00")
        self.root.update()

        x, y = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        
        self.root.withdraw()
        self.root.update()
        shot = ImageGrab.grab(bbox=(x, y, x + w, y + h), all_screens=True)
        frame = cv2.cvtColor(np.array(shot), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.root.deiconify()

        cw, ch = w / 4, h / 6
        flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))
        selected_font = cv2.FONT_HERSHEY_DUPLEX

        for r in range(6):
            for c in range(4):
                xs, ys, xe, ye = int(c*cw), int(r*ch), int((c+1)*cw), int((r+1)*ch)
                cell = gray[ys+25:ye-35, xs+25:xe-25]
                if cell.size == 0: continue
                kp, des = self.sift.detectAndCompute(cell, None)
                if des is None: continue

                best, m_max = None, 0
                for icon in self.icons_db:
                    try:
                        matches = flann.knnMatch(icon["des"], des, k=2)
                        good = [m for m, n in matches if m.distance < 0.7 * n.distance]
                        if len(good) > m_max: m_max, best = len(good), icon["name"]
                    except: continue

                if best and m_max > 8:
                    color, label = get_category_style(best)
                    item_name = best.replace("_", " ").upper()
                    cv2.rectangle(frame, (xs+5, ys+5), (xe-5, ye-5), color, 2)
                    cat_font_scale = 0.45
                    (tw_l, th_l), _ = cv2.getTextSize(label, selected_font, cat_font_scale, 1)
                    cv2.rectangle(frame, (xs+5, ys+5), (xs+tw_l+12, ys+22), (0,0,0), -1) 
                    cv2.putText(frame, label, (xs+8, ys+16), selected_font, cat_font_scale, color, 1, cv2.LINE_AA)
                    bar_h = 32
                    cv2.rectangle(frame, (xs+6, ye-bar_h-2), (xe-6, ye-6), (0,0,0), -1)
                    cv2.rectangle(frame, (xs+6, ye-bar_h-2), (xe-6, ye-6), color, 1)
                    font_scale = 0.7
                    while True:
                        (tw, th), _ = cv2.getTextSize(item_name, selected_font, font_scale, 1)
                        if tw <= (xe - xs) - 12 or font_scale <= 0.35: break
                        font_scale -= 0.05
                    text_x = xs + int((cw - tw) / 2)
                    text_y = (ye - bar_h) + int((bar_h + th) / 2) - 2
                    cv2.putText(frame, item_name, (text_x, text_y), selected_font, font_scale, (255,255,255), 1, cv2.LINE_AA)

        self.btn_scan.config(text="TARA", state="normal", fg="#00ff9d")
        
        win_name = "Arc Raider Scanner - Analysis Result"
        cv2.namedWindow(win_name)
        cv2.moveWindow(win_name, self.win_x + self.win_w + 50, self.win_y)
        cv2.imshow(win_name, frame)
        
        while True:
            if cv2.getWindowProperty(win_name, cv2.WND_PROP_VISIBLE) < 1:
                break
            self.root.update_idletasks()
            self.root.update()
            if cv2.waitKey(1) & 0xFF == 27:
                break
        
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = ArcRaiderScanner(root)
    root.mainloop()
