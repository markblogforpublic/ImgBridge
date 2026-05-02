@echo off
title Image Recognizer

echo =============================================
echo   Image Recognition Tool
echo   Dir: %~dp0
echo =============================================
echo.

cd /d "%~dp0"

python --version >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python first.
    echo         https://www.python.org/downloads/
    pause
    exit /b 1
)

python image_uploader.py
if errorlevel 1 (
    echo [ERROR] Run failed
    pause
)
