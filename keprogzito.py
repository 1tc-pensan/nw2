import tkinter as tk
from PIL import ImageGrab
import json
import os
import time

OUTPUT_COLOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "color.json")
OUTPUT_ZONE  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zone.json")
DELAY_SEC = 3


class ColorPicker:
    def __init__(self, screenshot):
        self.screenshot = screenshot
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.01)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")
        self.root.config(cursor="crosshair")

        self.root.bind("<ButtonPress-1>", self.on_click)
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.bind("<Motion>", self.on_move)

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
        with open(OUTPUT_COLOR, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Kivalasztott szin: R={r}  G={g}  B={b}  HEX=#{r:02X}{g:02X}{b:02X}")
        print(f"Mentve: {OUTPUT_COLOR}")
        input("Kesz! Nyomj Entert a kilepeshez...")


class ZonePicker:
    def __init__(self, screenshot):
        self.screenshot = screenshot
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.4)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")
        self.root.config(cursor="crosshair")

        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # háttér screenshot
        from PIL import ImageTk
        self.bg_img = ImageTk.PhotoImage(self.screenshot)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img)

        self.info = tk.Label(
            self.root,
            text="Huzd be azt a területet ahol a kristályok vannak!  (ESC = kilepes)",
            font=("Arial", 14, "bold"),
            fg="white", bg="#222222",
            padx=10, pady=6
        )
        self.info.place(relx=0.5, rely=0.03, anchor="center")

        self.start_x = self.start_y = 0
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="cyan", width=3
        )

    def on_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)

        if x2 - x1 < 20 or y2 - y1 < 20:
            return

        self.root.destroy()

        zone = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
        with open(OUTPUT_ZONE, "w") as f:
            json.dump(zone, f, indent=2)

        print(f"Zona mentve: ({x1}, {y1}) -> ({x2}, {y2})")
        input("Kesz! Nyomj Entert a kilepeshez...")


def main():
    print("=" * 50)
    print("  Kristaly segito")
    print("=" * 50)
    print("Mit szeretnel?")
    print("  1 - Szin kivalasztasa (kattints a kristályra)")
    print("  2 - Zona kivalasztasa (huzd be a területet ahol kereshet)")
    print()
    valasz = input("Valassz (1 vagy 2): ").strip()

    print(f"\nValtj at a jatekra! {DELAY_SEC} masodperc mulva jon az ablak...")
    time.sleep(DELAY_SEC)

    screenshot = ImageGrab.grab()

    if valasz == "1":
        app = ColorPicker(screenshot)
    else:
        app = ZonePicker(screenshot)

    app.root.mainloop()


if __name__ == "__main__":
    main()



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
