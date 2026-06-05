@echo off
chcp 65001 >nul
title Kristaly Auto-Klikker

echo ================================================
echo   Nextworld2 - Kristaly Auto-Klikker
echo ================================================
echo.

:: Python ellenőrzése
python --version >nul 2>&1
if errorlevel 1 (
    echo [HIBA] Python nincs telepitve!
    echo.
    echo Telepitsd innen: https://www.python.org/downloads/
    echo Fontos: telepitesnel pipald be az "Add Python to PATH" opciот!
    echo.
    pause
    exit /b 1
)

echo [OK] Python megtalalhato
echo.

:: Függőségek telepítése
echo Fuggosegek ellenorzese / telepitese...
python -m pip install pyautogui pillow opencv-python --quiet --disable-pip-version-check
if errorlevel 1 (
    echo [HIBA] Nem sikerult a csomagokat telepiteni!
    pause
    exit /b 1
)
echo [OK] Fuggosegek rendben
echo.

:: crystal.png ellenőrzése
if not exist "%~dp0crystal.png" (
    echo [HIBA] Nem talalom a crystal.png fajlt!
    echo.
    echo Mentsd el a kristaly kepet "crystal.png" nevvel
    echo ebbe a mappaba: %~dp0
    echo.
    pause
    exit /b 1
)

echo [OK] crystal.png megtalalhato
echo.
echo Indul a program... ^(Leallitas: Ctrl+C^)
echo.

:: Szkript futtatása
python "%~dp0crystal_clicker.py"

echo.
pause
