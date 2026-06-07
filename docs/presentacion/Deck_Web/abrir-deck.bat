@echo off
chcp 65001 >nul
cd /d "C:\LINA\TOOLS\cult-dashboard-starter"
echo ===========================================================
echo   Defensa de tesis - deck web (GeoAI Digital Twin / CGSM)
echo   Se abrira en el navegador: http://localhost:3000
echo   Deja ESTA ventana abierta mientras presentas.
echo   Para cerrarlo: presiona Ctrl+C o cierra la ventana.
echo ===========================================================
echo.
echo Iniciando servidor... (espera a que diga "Ready", ~5 s)
start "" cmd /c "timeout /t 7 >nul & start http://localhost:3000"
call npm run dev
pause
