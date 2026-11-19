@echo off
setlocal
cd /d "%~dp0"
set "PYTHONUTF8=1"
"%CD%\.venv\Scripts\python.exe" -u app.py
