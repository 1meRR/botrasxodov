@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ========================================
echo  Windows Voice Assistant - EXE Builder
echo  Folder: %CD%
echo ========================================

where py >nul 2>&1
if %errorlevel%==0 (
  set "PY=py -3.12"
) else (
  where python >nul 2>&1
  if %errorlevel%==0 (
    set "PY=python"
  ) else (
    echo [ERROR] Python not found in PATH.
    echo Install Python 3.12 and check "Add python.exe to PATH".
    goto :fail
  )
)

echo [1/4] Upgrading pip...
%PY% -m pip install --upgrade pip
if errorlevel 1 goto :fail

echo [2/4] Installing project dependencies...
%PY% -m pip install -r requirements.txt
if errorlevel 1 goto :fail

echo [3/4] Installing PyInstaller...
%PY% -m pip install pyinstaller==6.9.0
if errorlevel 1 goto :fail

echo [4/4] Building EXE...
%PY% -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --name WindowsVoiceAssistant ^
  --onefile ^
  --console ^
  --collect-all vosk ^
  --hidden-import pyttsx3.drivers.sapi5 ^
  main.py
if errorlevel 1 goto :fail

echo.
echo [OK] Build completed successfully.
echo EXE: %CD%\dist\WindowsVoiceAssistant.exe
echo.
pause
goto :eof

:fail
echo.
echo [FAILED] Build failed. See messages above.
echo.
pause
exit /b 1
