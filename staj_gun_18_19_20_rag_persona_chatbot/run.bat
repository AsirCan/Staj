@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: Kurulum kontrolü
if not exist ".venv" (
    echo [.venv] Sanal ortam bulunamadı. Kurulum otomatik başlatılıyor...
    call setup.bat
    exit /b 0
)

if not exist ".env" (
    copy .env.example .env >nul
)

set "PYTHON_EXE=.venv\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo Python sanal ortam çalıştırıcısı bulunamadı. Lütfen setup.bat dosyasını çalıştırın.
    pause
    exit /b 1
)

:: Uygulamayı Başlat
"%PYTHON_EXE%" "%~dp0run.py" %*

pause
