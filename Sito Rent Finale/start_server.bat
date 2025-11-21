@echo off
echo ========================================
echo   AutoUsateMilanoRent - Server Backend
echo ========================================
echo.
echo Avvio server in corso...
echo.

REM Verifica se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato!
    echo Installa Python da https://python.org
    pause
    exit /b 1
)

REM Installa dipendenze se necessario
echo Controllo dipendenze...
pip install -r requirements.txt

REM Avvia server
echo.
echo Avvio server Flask...
echo Server disponibile su: http://localhost:5000
echo.
python backend_server.py

pause





