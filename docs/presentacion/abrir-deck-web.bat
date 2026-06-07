@echo off
chcp 65001 >nul
cd /d "C:\LINA\TOOLS\cult-dashboard-starter"
echo ===========================================================
echo   Proyecto Programacion en SIG - deck web (Pipeline CGSM)
echo   Se abrira en el navegador: http://localhost:3000/prog
echo   La PRIMERA vez instala dependencias (tarda unos minutos).
echo   Deja ESTA ventana abierta mientras presentas.
echo   Para cerrarlo: presiona Ctrl+C o cierra la ventana.
echo ===========================================================
echo.
if not exist "node_modules" (
  echo Instalando dependencias por primera vez...
  call npm install
)
echo Iniciando servidor... (espera a que diga "Ready", ~5 s)
start "" cmd /c "timeout /t 8 >nul & start http://localhost:3000/prog"
call npm run dev
pause
