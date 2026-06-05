import tkinter as tk
from PIL import ImageGrab
import json
import os
import time

# ============================================================
#  Kristaly szinkod-szedo
#  Hasznalat:
#    1. Inditsd el ezt a szkriptet
#    2. Valtj at a jatekra (3 masodperc mulva jon az ablak)
#    3. Kattints ra a kristályra
#    4. Menti a szint a color.json fajlba
# ============================================================

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "color.json")
DELAY_SEC = 3


class ColorPicker:
    def __init__(self, screenshot):
        self.screenshot = screenshot
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.01)  # majdnem teljesen atlatszo
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")
        self.root.title("Kattints a kristályra!")
        self.root.config(cursor="crosshair")

        self.root.bind("<ButtonPress-1>", self.on_click)
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.bind("<Motion>", self.on_move)

        # info ablak
        self.info = tk.Label(
            self.root,
            text="Kattints a kristályra!  (ESC = kilepes)",
            font=("Arial", 14, "bold"),
            fg="white", bg="#222222",
            padx=10, pady=6
        )
        self.info.place(relx=0.5, rely=0.03, anchor="center")

        self.color_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12),
            fg="white", bg="#222222",
            padx=10, pady=4
        )
        self.color_label.place(relx=0.5, rely=0.09, anchor="center")

    def on_move(self, event):
        try:
            r, g, b = self.screenshot.getpixel((event.x, event.y))
            self.color_label.config(text=f"Szin: R={r}  G={g}  B={b}   HEX=#{r:02X}{g:02X}{b:02X}")
        except Exception:
            pass

    def on_click(self, event):
        try:
            r, g, b = self.screenshot.getpixel((event.x, event.y))
        except Exception:
            return
        self.root.destroy()

        data = {"r": r, "g": g, "b": b, "hex": f"#{r:02X}{g:02X}{b:02X}"}
        with open(OUTPUT_FILE, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Kivalasztott szin: R={r}  G={g}  B={b}  HEX=#{r:02X}{g:02X}{b:02X}")
        print(f"Mentve: {OUTPUT_FILE}")
        input("Kesz! Nyomj Entert a kilepeshez...")


def main():
    print("=" * 50)
    print("  Kristaly szinkod-szedo")
    print("=" * 50)
    print(f"Valtj at a jatekra! {DELAY_SEC} masodperc mulva jon a valaszto...")
    time.sleep(DELAY_SEC)

    screenshot = ImageGrab.grab()
    app = ColorPicker(screenshot)
    app.root.mainloop()


if __name__ == "__main__":
    main()
    print("  Kristaly keprogzito")
    print("=" * 50)
    print(f"Valtj at a jatekra! {DELAY_SEC} masodperc mulva jon a kivalaszto ablak...")

    import time
    time.sleep(DELAY_SEC)

    app = ScreenCapture()
    app.root.mainloop()


if __name__ == "__main__":
    main()
