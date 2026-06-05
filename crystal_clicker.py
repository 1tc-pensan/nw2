import pyautogui
import time
import sys
import os
import json
import ctypes
import ctypes.wintypes
import numpy as np
from PIL import ImageGrab

# ============================================================
#  Nextworld2 - Kristaly auto-klikker (szin alapu)
#  Hasznalat:
#    1. Futtasd a keprogzito.py-t es kattints a kristályra
#    2. Inditsd el ezt a szkriptet
#    3. Nyomj Ctrl+C a leallitashoz
# ============================================================

COLOR_FILE   = "color.json"   # a szinkod fajl neve
ZONE_FILE    = "zone.json"    # a zona fajl neve (opcionalis)
TOLERANCE    = 30             # szintoleranacia (0-255, minnel nagyobb annál több szint fogad el)
CLICK_DELAY  = 5.0            # varakozas kattintasok kozott (masodperc)
MIN_PIXELS   = 30             # legalabb ennyi egyezo pixel kell hogy kattintson
LOOP         = True


def load_color(color_file):
    with open(color_file, "r") as f:
        data = json.load(f)
    return data["r"], data["g"], data["b"]


def load_zone(zone_file):
    if not os.path.exists(zone_file):
        return None
    with open(zone_file, "r") as f:
        z = json.load(f)
    return z["x1"], z["y1"], z["x2"], z["y2"]


def find_and_click(target_r, target_g, target_b, tolerance, min_pixels, zone=None):
    if zone:
        x1, y1, x2, y2 = zone
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        offset_x, offset_y = x1, y1
    else:
        screenshot = ImageGrab.grab()
        offset_x, offset_y = 0, 0

    img = np.array(screenshot)

    # Szin egyezes keresese toleranciaval
    mask = (
        (np.abs(img[:, :, 0].astype(int) - target_r) <= tolerance) &
        (np.abs(img[:, :, 1].astype(int) - target_g) <= tolerance) &
        (np.abs(img[:, :, 2].astype(int) - target_b) <= tolerance)
    )

    ys, xs = np.where(mask)

    if len(xs) < min_pixels:
        print(f"Nem talaltam kristalyt ({len(xs)} egyezo pixel, minimum: {min_pixels})")
        return False

    # Legközelebbi pixel a cursorhoz
    cursor_x, cursor_y = pyautogui.position()
    abs_xs = xs + offset_x
    abs_ys = ys + offset_y
    distances = np.sqrt((abs_xs - cursor_x) ** 2 + (abs_ys - cursor_y) ** 2)
    nearest_idx = np.argmin(distances)

    click_x = int(abs_xs[nearest_idx])
    click_y = int(abs_ys[nearest_idx])

    pyautogui.moveTo(click_x, click_y, duration=0.3)
    time.sleep(0.15)
    pyautogui.click(button='left')
    time.sleep(0.1)
    print(f"Kattintottam: ({click_x}, {click_y})  |  {len(xs)} egyezo pixel")
    return True


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    color_path = os.path.join(script_dir, COLOR_FILE)

    if not os.path.exists(color_path):
        print("HIBA: Nem talalom a color.json fajlt!")
        print("Futtasd elobb a keprogzito.py-t es kattints a kristályra!")
        input("Nyomj Entert a kilepeshez...")
        sys.exit(1)

    target_r, target_g, target_b = load_color(color_path)

    zone_path = os.path.join(script_dir, ZONE_FILE)
    zone = load_zone(zone_path)

    print("=" * 50)
    print("  Nextworld2 Kristaly Auto-Klikker (szin alapu)")
    print("=" * 50)
    print(f"Cel szin: R={target_r}  G={target_g}  B={target_b}")
    print(f"Tolerancia: +/-{TOLERANCE}")
    if zone:
        print(f"Zona: ({zone[0]}, {zone[1]}) -> ({zone[2]}, {zone[3]})")
    else:
        print("Zona: nincs beallitva (egesz kepernyo)")
    print("Leallitas: Ctrl+C  |  Veszjel: egeret sarokba")
    print("=" * 50)
    print()

    # Konzol minimalizalasa
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 6)

    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1

    try:
        if LOOP:
            print("Folyamatos kereses modban futok...\n")
            while True:
                find_and_click(target_r, target_g, target_b, TOLERANCE, MIN_PIXELS, zone)
                time.sleep(CLICK_DELAY)
        else:
            find_and_click(target_r, target_g, target_b, TOLERANCE, MIN_PIXELS, zone)
    except KeyboardInterrupt:
        print("\nLeallitva.")


if __name__ == "__main__":
    main()

# ============================================================
#  Nextworld2 - Kristály auto-klikker
#  Használat:
#    1. Mentsd el a kristály képét: 'crystal.png' néven
#       (ebbe a mappába, ahol ez a szkript van)
#    2. Indítsd el ezt a szkriptet
#    3. Nyomj Ctrl+C a leállításhoz
# ============================================================

CRYSTAL_IMAGE = "crystal.png"   # a kép neve
CONFIDENCE   = 0.4              # egyezés szintje (0.0 - 1.0)
CLICK_DELAY  = 4.0              # várakozás kattintások között (másodperc)
LOOP         = True             # True = folyamatosan keres, False = csak egyszer


def find_and_click(image_path, confidence=0.8):
    """Megkeresi az összes kristályt és a cursorhoz legközelebb lévőre kattint."""
    try:
        locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence, grayscale=True))
        if not locations:
            print("Nem talaltam kristalyt a kepernyon...")
            return False

        cursor_x, cursor_y = pyautogui.position()

        def distance(loc):
            cx, cy = pyautogui.center(loc)
            return ((cx - cursor_x) ** 2 + (cy - cursor_y) ** 2) ** 0.5

        closest = min(locations, key=distance)
        center = pyautogui.center(closest)
        pyautogui.moveTo(center.x, center.y, duration=0.3)
        time.sleep(0.15)
        pyautogui.click(button='left')
        time.sleep(0.1)
        print(f"Kattintottam ({len(locations)} talalat kozul a legkozelebbit): ({center.x}, {center.y})")
        return True
    except Exception:
        print("Nem talaltam kristalyt a kepernyon...")
        return False


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, CRYSTAL_IMAGE)

    if not os.path.exists(image_path):
        print(f"HIBA: Nem találom a képfájlt: {image_path}")
        print(f"Mentsd el a kristály képét '{CRYSTAL_IMAGE}' névvel ebbe a mappába:")
        print(f"  {script_dir}")
        input("Nyomj Entert a kilépéshez...")
        sys.exit(1)

    print("=" * 50)
    print("  Nextworld2 Kristály Auto-Klikker")
    print("=" * 50)
    print(f"Kép: {image_path}")
    print(f"Egyezési szint: {CONFIDENCE}")
    print("Leállítás: Ctrl+C  |  Vészkijárat: húzd az egeret sarokba")
    print("=" * 50)
    print()

    # Konzol ablak minimalizalasa hogy a jatek legyen fokuszban
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 6)  # SW_MINIMIZE = 6

    # PyAutoGUI biztonsági beállítások
    pyautogui.FAILSAFE = True   # egér sarkába húzva leáll
    pyautogui.PAUSE = 0.1

    try:
        if LOOP:
            print("Folyamatos keresés módban futok...\n")
            while True:
                find_and_click(image_path, CONFIDENCE)
                time.sleep(CLICK_DELAY)
        else:
            print("Egyszer keresek...\n")
            find_and_click(image_path, CONFIDENCE)
    except KeyboardInterrupt:
        print("\nLeállítva.")


if __name__ == "__main__":
    main()
