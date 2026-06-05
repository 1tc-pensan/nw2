import tkinter as tk
from PIL import ImageGrab
import os
import sys

# ============================================================
#  Kristaly keprogzito
#  Hasznalat:
#    1. Indítsd el ezt a szkriptet
#    2. Valtj at a jatekra (3 masodperc mulva jon az ablak)
#    3. Huzd be a kristaly kore a téglalapot
#    4. Keszul a crystal.png
# ============================================================

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crystal.png")
DELAY_SEC = 3


class ScreenCapture:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")
        self.root.title("Jelold ki a kristalyt")

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        label = tk.Label(
            self.root,
            text="Huzd be a kristaly kore a negyzetett, majd engedd el!  (ESC = kilepes)",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="black"
        )
        label.place(relx=0.5, rely=0.05, anchor="center")

        self.start_x = self.start_y = 0
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="red", width=2
        )

    def on_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        end_x, end_y = event.x, event.y
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        if x2 - x1 < 5 or y2 - y1 < 5:
            return

        self.root.destroy()

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save(OUTPUT_FILE)
        print(f"Mentve: {OUTPUT_FILE}  ({x2-x1}x{y2-y1} px)")
        input("Kesz! Nyomj Entert a kilepeshez...")


def main():
    print("=" * 50)
    print("  Kristaly keprogzito")
    print("=" * 50)
    print(f"Valtj at a jatekra! {DELAY_SEC} masodperc mulva jon a kivalaszto ablak...")

    import time
    time.sleep(DELAY_SEC)

    app = ScreenCapture()
    app.root.mainloop()


if __name__ == "__main__":
    main()
