@echo off
REM Starts the LeetCode study website at http://localhost:8000
cd /d "%~dp0"
start "" http://localhost:8000/
python -m http.server 8000 --bind 127.0.0.1
