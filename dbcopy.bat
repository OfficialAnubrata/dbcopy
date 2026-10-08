@echo off
rem Double-click to start the dbcopy dashboard and open it in its own app window.
cd /d "%~dp0"

rem Start the server minimized (skipped harmlessly if one is already running).
start "dbcopy server" /min uv run python main.py

rem Wait until the dashboard answers.
:wait
timeout /t 1 /nobreak >nul
curl -s -o nul http://127.0.0.1:8000/ || goto wait

rem Edge's --app mode = standalone window, no tabs or address bar.
start "" msedge --app=http://127.0.0.1:8000/
