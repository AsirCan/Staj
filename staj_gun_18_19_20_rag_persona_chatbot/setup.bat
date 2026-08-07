@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ============================================================
echo   KANYE WEST LYRIC & PERSONA ARCHIVE - OTOMATİK KURULUM
echo ============================================================
echo.

:: 1. Python kontrolü
set "PY_CMD="
python --version >nul 2>&1
if !errorlevel! equ 0 (
    set "PY_CMD=python"
) else (
    py -3 --version >nul 2>&1
    if !errorlevel! equ 0 (
        set "PY_CMD=py -3"
    )
)

if "%PY_CMD%"=="" (
    echo [HATA] Sistemde Python bulunamadı!
    echo Lütfen Python 3.10 veya üzeri bir sürüm yükleyip PATH'e ekleyin.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/5] Python algılandı: %PY_CMD%
echo.

:: 2. Sanal Ortam (.venv) Oluşturma
if not exist ".venv" (
    echo [2/5] Sanal ortam (.venv) oluşturuluyor...
    %PY_CMD% -m venv .venv
    if !errorlevel! neq 0 (
        echo [HATA] Sanal ortam oluşturulamadı!
        pause
        exit /b 1
    )
    echo Sanal ortam başarıyla oluşturuldu.
) else (
    echo [2/5] Sanal ortam (.venv) zaten mevcut.
)
echo.

set "VENV_PY=.venv\Scripts\python.exe"

:: 3. Bağımlılıkları Yükleme
echo [3/5] Gerekli Python kütüphaneleri yüklüyor/güncelleniyor...
"%VENV_PY%" -m pip install --upgrade pip >nul 2>&1
"%VENV_PY%" -m pip install -r requirements.txt
if !errorlevel! neq 0 (
    echo [HATA] Bağımlılıklar yüklenirken bir sorun oluştu.
    pause
    exit /b 1
)
echo.

:: 4. Ayar (.env) Dosyası Kontrolü
if not exist ".env" (
    echo [4/5] .env ayar dosyası .env.example'dan kopyalanıyor...
    copy .env.example .env >nul
) else (
    echo [4/5] .env ayar dosyası mevcut.
)
echo.

:: 5. Vektör Veritabanı (ChromaDB) İndeks Kontrolü
if not exist "data\chroma" (
    echo [5/5] Vektör veritabanı (ChromaDB) bulunamadı. Otomatik indeksleniyor...
    "%VENV_PY%" scripts\collect_lyrics.py --confirm-permission --delay 1.0
    "%VENV_PY%" scripts\build_index.py --reset
) else (
    echo [5/5] Vektör veritabanı (ChromaDB) hazır.
)
echo.

echo ============================================================
echo   KURULUM TAMAMLANDI! 
echo ============================================================
echo.
echo Uygulamayı başlatmak için run.bat dosyasını çalıştırabilirsiniz.
echo.
set /p LAUNCH="Şimdi uygulamayı başlatmak ister misiniz? (Y/N): "
if /i "%LAUNCH%"=="Y" (
    "%VENV_PY%" run.py
)

pause
