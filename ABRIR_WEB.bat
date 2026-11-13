@echo off
cd /d "%~dp0"
echo Abriendo Entre cepas en http://localhost:8000 (cierra esta ventana para parar el servidor)
start "" http://localhost:8000
(python -m http.server 8000) || (py -m http.server 8000)
