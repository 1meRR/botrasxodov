@echo off
setlocal

REM Build standalone EXE for Windows 10/11
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller==6.9.0

pyinstaller ^
  --noconfirm ^
  --clean ^
  --name WindowsVoiceAssistant ^
  --onefile ^
  --console ^
  --collect-all vosk ^
  --hidden-import pyttsx3.drivers.sapi5 ^
  main.py

echo.
echo Build completed. EXE: dist\WindowsVoiceAssistant.exe
endlocal
