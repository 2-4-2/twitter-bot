@echo off
REM Twitter Bot Hizli Kurulum - Windows

echo.
echo ===================================
echo    Twitter Bot Kurulum Basladi
echo ===================================
echo.

REM Python kontrolu
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [HATA] Python bulunamadi! Python 3.8+ yukleyin.
    pause
    exit /b 1
)

echo [OK] Python yuklendi
echo.

REM Paketleri kur
echo [INFO] Python paketleri yukleniyor...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [HATA] Paket yukleme basarisiz!
    pause
    exit /b 1
)

echo [OK] Paketler yuklendi!
echo.

REM .env dosyasi kontrolu
if not exist ".env" (
    echo [INFO] .env dosyasi olusturuluyor...
    copy .env.example .env
    echo.
    echo [UYARI] .env dosyasini duzenleyip API anahtarlarini ekleyin!
    echo.
    echo Gerekli API Anahtarlari:
    echo   1. Twitter API Keys (5 adet)
    echo   2. Anthropic API Key (1 adet)
    echo.
    echo Detayli rehber icin: KURULUM_REHBERI.md dosyasini okuyun
    echo.
)

REM Logo kontrolu
if not exist "omt_logo.png" (
    echo [UYARI] Logo dosyasi (omt_logo.png) bulunamadi!
    echo          Logo olmadan da calisir ama gorsellere logo eklenmez.
    echo.
)

echo [OK] Kurulum tamamlandi!
echo.
echo Sonraki adimlar:
echo   1. notepad .env    (API anahtarlarini ekle)
echo   2. python twitter_bot_fixed.py    (Botu calistir)
echo.
echo 24/7 calistirma icin: KURULUM_REHBERI.md dosyasina bakin
echo.

pause
