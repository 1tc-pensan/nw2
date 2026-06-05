import pyautogui
import time
import sys
import os

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
        locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
        if not locations:
            print("✗ Nem találtam kristályt a képernyőn...")
            return False

        cursor_x, cursor_y = pyautogui.position()

        def distance(loc):
            cx, cy = pyautogui.center(loc)
            return ((cx - cursor_x) ** 2 + (cy - cursor_y) ** 2) ** 0.5

        closest = min(locations, key=distance)
        center = pyautogui.center(closest)
        pyautogui.moveTo(center.x, center.y, duration=0.3)
        pyautogui.click()
        print(f"✓ Legközelebbi kristály ({len(locations)} db közül): ({center.x}, {center.y})")
        return True
    except Exception:
        print("✗ Nem találtam kristályt a képernyőn...")
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
