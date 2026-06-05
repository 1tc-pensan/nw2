@echo off
title Kristaly Auto-Klikker

echo ================================================
echo   Nextworld2 - Kristaly Auto-Klikker
echo ================================================
echo.

:: Python ellenorzese
python --version >nul 2>&1
if errorlevel 1 (
    echo [HIBA] Python nincs telepitve!
    echo.
    echo Telepitsd innen: https://www.python.org/downloads/
    echo Fontos: pipald be az "Add Python to PATH" opcioth!
    echo.
    pause
    exit /b 1
)

echo [OK] Python megtalalhato
echo.

:: Fuggosegek telepitese
echo Fuggosegek ellenorzese / telepitese...
python -m pip install pyautogui pillow opencv-python --quiet --disable-pip-version-check
if errorlevel 1 (
    echo [HIBA] Nem sikerult a csomagokat telepiteni!
    pause
    exit /b 1
)
echo [OK] Fuggosegek rendben
echo.

:: crystal.png ellenorzese
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
echo.echo Mit szeretnel?
echo   1 - Kristaly keprogzito inditasa (uj crystal.png keszitese)
echo   2 - Auto-klikker inditasa
echo.
set /p valasz="Valassz (1 vagy 2): "

if "%valasz%"=="1" (
    echo.
    echo Indul a keprogzito...
    python "%~dp0keprogzito.py"
    goto :eof
)

echo.echo Indul a program... (Leallitas: Ctrl+C)
echo.

:: Szkript futtatása
python "%~dp0crystal_clicker.py"

echo.
pause
