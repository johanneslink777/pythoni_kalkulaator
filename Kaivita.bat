@echo off
cd /d "%~dp0"
if exist "%USERPROFILE%\AppData\Local\Python\pythoncore-3.15-64\python.exe" (
  "%USERPROFILE%\AppData\Local\Python\pythoncore-3.15-64\python.exe" mootor.py
) else (
  py mootor.py
)
if errorlevel 1 pause
